from abc import abstractmethod
import numpy as np
import tensorflow as tf
from common import utils
from common.model import BaseModel
from deepemb.default_custom import DefaultSkipThoughtTransform


class DeepEmbModel(BaseModel):
    def __init__(self, session, transformer, config):
        super(DeepEmbModel, self).__init__(session, transformer, config)
        self.doc_vector = None

    @abstractmethod
    def vectors(self, docs):
        pass


class GraphSkipThoughtModel(DeepEmbModel):
    def __init__(self, model_path, config, TransformClass=None):
        if TransformClass is None:
            super(GraphSkipThoughtModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), DefaultSkipThoughtTransform(config), config)
        else:
            super(GraphSkipThoughtModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), TransformClass(config), config)
        self.transformer.load_pre_data()
        self.session.as_default()

        self.input = self.session.graph.get_tensor_by_name(self.scope+'encode:0')
        self.input_lengths = self.session.graph.get_tensor_by_name(self.scope+'input_lengths:0')

        self.output_prev_input = self.session.graph.get_tensor_by_name(self.scope+'output_prev_input:0')
        self.output_prev_target = self.session.graph.get_tensor_by_name(self.scope+'output_prev_target:0')
        self.output_prev_lengths = self.session.graph.get_tensor_by_name(self.scope+'output_prev_lengths:0')

        self.output_post_input = self.session.graph.get_tensor_by_name(self.scope+'output_post_input:0')
        self.output_post_target = self.session.graph.get_tensor_by_name(self.scope+'output_post_target:0')
        self.output_post_lengths = self.session.graph.get_tensor_by_name(self.scope+'output_post_lengths:0')

        self.input_keep_prob = self.session.graph.get_tensor_by_name(self.scope+"input_keep_prob:0")
        self.output_keep_prob = self.session.graph.get_tensor_by_name(self.scope+"output_keep_prob:0")

        self.doc_vector = self.session.graph.get_tensor_by_name(self.scope+"encoder/rnn/while/Exit_3:0")

        self.prev_logits = self.session.graph.get_tensor_by_name(self.scope+"softmax_prev_prediction/logits:0")
        self.prev_prediction = self.session.graph.get_tensor_by_name(self.scope+"softmax_prev_prediction/prev_prediction:0")
        self.prev_state = self.session.graph.get_tensor_by_name(self.scope+"decoder_prev_prediction/rnn/while/Exit_3:0")
        self.post_logits = self.session.graph.get_tensor_by_name(self.scope+"softmax_post_prediction/logits:0")
        self.post_prediction = self.session.graph.get_tensor_by_name(self.scope+"softmax_post_prediction/post_prediction:0")
        self.post_state = self.session.graph.get_tensor_by_name(self.scope+"decoder_post_prediction/rnn/while/Exit_3:0")

    def gen(self, doc):
        doc_ids = self.transformer.transform_parts([doc])
        doc_lens = np.array([len(d) for d in [doc]])
        start_word_id = self.transformer.w2id["<LM_START_LABEL>"]
        end_word_id = self.transformer.w2id["<LM_END_LABEL>"]

        counter = 0
        prev_decode_seq = [[start_word_id]]
        while prev_decode_seq[0][-1] != end_word_id:
            feed_dict = {self.input: doc_ids,
                         self.input_lengths: doc_lens,
                         self.output_prev_input: prev_decode_seq,
                         self.output_prev_lengths: [len(prev_decode_seq[0])],
                         self.input_keep_prob: 1.0,
                         self.output_keep_prob: 1.0}
            predict, state = self.session.run([self.prev_prediction, self.prev_state], feed_dict=feed_dict)
            word = np.argmax(predict, 1)[-1]
            prev_decode_seq[0] += [word]
            counter += 1
            if counter > self.config.seq_cut_length:
                break

        counter = 0
        post_decode_seq = [[start_word_id]]
        while post_decode_seq[0][-1] != end_word_id:
            feed_dict = {self.input: doc_ids,
                         self.input_lengths: doc_lens,
                         self.output_post_input: post_decode_seq,
                         self.output_post_lengths: [len(post_decode_seq[0])],
                         self.input_keep_prob: 1.0,
                         self.output_keep_prob: 1.0}
            predict, state = self.session.run([self.post_prediction, self.post_state], feed_dict=feed_dict)
            word = np.argmax(predict, 1)[-1]
            post_decode_seq[0] += [word]
            counter += 1
            if counter > self.config.seq_cut_length:
                break

        prev_seq = [self.transformer.id2w[p] for p in prev_decode_seq[0]]
        post_seq = [self.transformer.id2w[p] for p in post_decode_seq[0]]
        return prev_seq, post_seq

    def vectors(self, docs):
        doc_ids = self.transformer.transform_parts(docs)
        doc_lens = np.array([len(d) for d in docs])
        feed_dict = {self.input: doc_ids,
                     self.input_lengths: doc_lens,
                     self.input_keep_prob: 1.0,
                     self.output_keep_prob: 1.0}

        return self.session.run([self.doc_vector], feed_dict=feed_dict)[0]

