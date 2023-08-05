import tensorflow as tf
from common import utils
import numpy as np
import logging
from common.model import BaseModel
from .default_custom import DeepLMTransform


class DeepLMModel(BaseModel):
    def __init__(self, session, transformer, config):
        super(DeepLMModel, self).__init__(session, transformer, config)
        self.input = None
        self.labels = None
        self.sequence_lengths = None
        self.input_keep_prob = None
        self.output_keep_prob = None
        self.hidden_output = None
        self.logits = None
        self.probs = None
        self.sequence_scores = None

    def fluency(self, multi_parts):
        part_ids = self.transformer.transform_parts(multi_parts)
        part_lens = [len(parts)+1 for parts in multi_parts]
        feed_dict = {self.input: part_ids[:,:-1],
                     self.labels: part_ids[:,1:],
                     self.sequence_lengths: np.array(part_lens),
                     self.input_keep_prob: 1.0,
                     self.output_keep_prob: 1.0}

        sequence_scores = self.session.run([self.sequence_scores], feed_dict=feed_dict)[0]
        log_scores = np.log(sequence_scores)/np.log(2)
        scores = []
        for s, l in zip(log_scores, part_lens):
            s[l-1:] = 0
            scores.append(s)
        scores = np.sum(np.array(scores), axis=1)
        return 1 / (1 - scores / part_lens)

    def hidden_output(self, multi_parts):
        part_ids = self.transformer.transform_parts(multi_parts)
        part_lens = [len(parts) for parts in multi_parts]
        feed_dict = {self.input: part_ids,
                     self.sequence_lengths: np.array(part_lens),
                     self.input_keep_prob: 1.0,
                     self.output_keep_prob: 1.0}

        hidden_output = self.session.run([self.hidden_output], feed_dict=feed_dict)
        return hidden_output


class GraphDeepLMModel(DeepLMModel):
    def __init__(self, model_path, config, TransformClass=None):
        if TransformClass is None:
            super(GraphDeepLMModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), DeepLMTransform(config), config)
        else:
            super(GraphDeepLMModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), TransformClass(config), config)
        self.transformer.load_pre_data()
        self.session.as_default()
        self.input = self.session.graph.get_tensor_by_name("input:0")
        self.labels = self.session.graph.get_tensor_by_name("labels:0")
        self.sequence_lengths = self.session.graph.get_tensor_by_name("sequence_lengths:0")
        self.input_keep_prob = self.session.graph.get_tensor_by_name("input_keep_prob:0")
        self.output_keep_prob = self.session.graph.get_tensor_by_name("output_keep_prob:0")
        self.logits = self.session.graph.get_tensor_by_name("logits/logits:0")
        self.probs = self.session.graph.get_tensor_by_name("logits/probs:0")
        self.hidden_output = self.session.graph.get_tensor_by_name("hidden_output:0")
        self.sequence_scores = self.session.graph.get_tensor_by_name("scores/sequence_scores:0")


class Bi_GRU_LM(DeepLMModel):
    def __init__(self, session, transformer, config):
        super(Bi_GRU_LM, self).__init__(session, transformer, config)
        self.input = tf.placeholder(tf.int32, shape=[None, None], name="input")
        self.labels = tf.placeholder(tf.int32, shape=[None, None], name="labels")
        self.sequence_lengths = tf.placeholder(tf.int32, shape=[None], name="sequence_lengths")
        self.weights = tf.placeholder(tf.float32, shape=[None, None], name="weights")
        self.input_keep_prob = tf.placeholder(tf.float32, name="input_keep_prob")
        self.output_keep_prob = tf.placeholder(tf.float32, name="output_keep_prob")

        def gru_cell():
            gru = tf.contrib.rnn.GRUCell(config.hidden_size)
            gru = tf.contrib.rnn.DropoutWrapper(cell=gru, input_keep_prob=self.input_keep_prob,
                                                output_keep_prob=self.output_keep_prob)
            return gru

        # embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            logging.info("Init embedding with xavier initializer.")
            embedding_initializer = tf.contrib.layers.xavier_initializer()
            self._W = tf.get_variable("W", shape=[transformer.vocab_size, self.config.embedding_size],
                                      initializer=embedding_initializer,
                                      dtype=tf.float32)
            inputs = tf.nn.embedding_lookup(self._W, self.input)

        fw_cell = tf.contrib.rnn.MultiRNNCell([gru_cell() for _ in range(self.config.hidden_layer_num)], state_is_tuple=True)
        bw_cell = tf.contrib.rnn.MultiRNNCell([gru_cell() for _ in range(self.config.hidden_layer_num)], state_is_tuple=True)

        (output_fw_seq, output_bw_seq), _ = tf.nn.bidirectional_dynamic_rnn(fw_cell, bw_cell, inputs,
                                                                            sequence_length=self.sequence_lengths,
                                                                            dtype=tf.float32,
                                                                            scope='dynamic_rnn_layer')
        output = tf.concat([output_fw_seq, output_bw_seq], axis=-1, name="output")
        output_shape = tf.shape(output)
        self.hidden_output = tf.reshape(output, [-1, 2*config.hidden_size], name="hidden_output")

        with tf.variable_scope("logits"):
            W = tf.get_variable("W", shape=[2 * config.hidden_size, transformer.vocab_size],
                                initializer=tf.contrib.layers.xavier_initializer(),
                                dtype=tf.float32)

            b = tf.get_variable("b", shape=[transformer.vocab_size],
                                initializer=tf.zeros_initializer(),
                                dtype=tf.float32)

            logits_fc = tf.nn.xw_plus_b(self.hidden_output, W, b)
            self.logits = tf.reshape(logits_fc, [-1, output_shape[1], transformer.vocab_size], name="logits")
            self.probs = tf.nn.softmax(logits=self.logits, name="probs")

        with tf.variable_scope("loss"):
            self.loss = tf.contrib.seq2seq.sequence_loss(self.logits, self.labels, self.weights, name="loss")

        with tf.variable_scope("scores"):
            batch_size = tf.shape(self.probs)[0]
            max_seq_len = tf.shape(self.probs)[1]
            num_tags = transformer.vocab_size

            flattened_logits = tf.reshape(self.probs, [-1])

            offsets = tf.expand_dims(tf.range(batch_size) * max_seq_len * num_tags, 1)
            offsets += tf.expand_dims(tf.range(max_seq_len) * num_tags, 0)

            flattened_tag_indices = tf.reshape(offsets + self.labels, [-1])

            self.sequence_scores = tf.reshape(tf.gather(flattened_logits, flattened_tag_indices),
                                              [batch_size, max_seq_len], name="sequence_scores")

    def save(self, output_path):
        save_graph_value_scopes = [self.scope+"logits/probs", self.scope+"logits/logits", self.scope+"scores/sequence_scores"]
        logging.info(save_graph_value_scopes)
        graph = tf.graph_util.convert_variables_to_constants(self.session, self.session.graph_def, save_graph_value_scopes)
        with tf.gfile.GFile(output_path+".pb", "wb") as f:
            f.write(graph.SerializeToString())

