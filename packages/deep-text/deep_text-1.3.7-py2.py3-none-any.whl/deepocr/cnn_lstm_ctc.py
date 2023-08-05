import tensorflow as tf
from .model import DeepOCRModel
import logging
import warpctc_tensorflow

DEFAULT_PADDING = 'SAME'


class CNN_LSTM_CTC(DeepOCRModel):
    def __init__(self, session, transformer, config):
        super(CNN_LSTM_CTC, self).__init__(session, transformer, config)
        self.input = tf.placeholder(tf.float32, shape=[None, None, None, None], name="input")
        self.labels = tf.placeholder(tf.int32, shape=[None], name="labels")
        self.sequence_lengths = tf.placeholder(tf.int32, shape=[None], name="sequence_lengths")
        self.label_lengths = tf.placeholder(tf.int32, shape=[None], name="label_lengths")
        self.input_keep_prob = tf.placeholder(tf.float32, name="input_keep_prob")
        self.output_keep_prob = tf.placeholder(tf.float32, name="output_keep_prob")

        cnn_layer = self.cnn(self.input)
        logits, self.dense_decoded = self.lstm(cnn_layer, self.sequence_lengths)

        ctc_loss = warpctc_tensorflow.ctc(activations=logits, flat_labels=self.labels,
                                          label_lengths=self.label_lengths, input_lengths=self.sequence_lengths)
        self.loss = tf.reduce_mean(ctc_loss)

    def cnn(self, cnn_input):
        conv_layer_1_1 = self.conv(cnn_input, 3, 3, 64, 1, 1, c_i=self.config.n_channels, name='conv1_1')
        conv_layer_1_2 = self.conv(conv_layer_1_1, 3, 3, 64, 1, 1, name='conv1_2')
        max_pool_1 = self.max_pool(conv_layer_1_2, 2, 2, 2, 2, padding='VALID', name='pool1')

        conv_layer_2_1 = self.conv(max_pool_1, 3, 3, 128, 1, 1, name='conv2_1')
        conv_layer_2_2 = self.conv(conv_layer_2_1, 3, 3, 128, 1, 1, name='conv2_2')
        max_pool_2 = self.max_pool(conv_layer_2_2, 2, 2, 2, 2, padding='VALID', name='pool2')

        conv_layer_3_1 = self.conv(max_pool_2, 3, 3, 256, 1, 1, name='conv3_1')
        conv_layer_3_2 = self.conv(conv_layer_3_1, 3, 3, 256, 1, 1, name='conv3_2')
        conv_layer_3_3 = self.conv(conv_layer_3_2, 3, 3, 256, 1, 1, name='conv3_3')
        max_pool_3 = self.max_pool(conv_layer_3_3, 2, 2, 2, 2, padding='VALID', name='pool3')

        conv_layer_4_1 = self.conv(max_pool_3, 3, 3, 512, 1, 1, name='conv4_1', bn=True)
        conv_layer_4_2 = self.conv(conv_layer_4_1, 3, 3, 512, 1, 1, name='conv4_2', bn=True)
        conv_layer_4_3 = self.conv(conv_layer_4_2, 3, 3, 512, 1, 1, name='conv4_3', bn=True)
        max_pool_4 = self.max_pool(conv_layer_4_3, 2, 2, 2, 2, padding='VALID', name='pool4')

        conv_layer_5_1 = self.conv(max_pool_4, 3, 3, 512, 1, 1, name='conv5_1', bn=True)
        conv_layer_5_2 = self.conv(conv_layer_5_1, 3, 3, 512, 1, 1, name='conv5_2', bn=True)
        conv_layer_5_3 = self.conv(conv_layer_5_2, 3, 3, 512, 1, 1, name='conv5_3', bn=True)

        input_shape = tf.shape(conv_layer_5_3)
        return tf.reshape(conv_layer_5_3, [input_shape[0], input_shape[1]*input_shape[2], 512])

    def lstm(self, inputs, sequence_lengths):
        fw_cell = tf.contrib.rnn.MultiRNNCell([self.gru_cell() for _ in range(self.config.hidden_layer_num)],
                                              state_is_tuple=True)
        bw_cell = tf.contrib.rnn.MultiRNNCell([self.gru_cell() for _ in range(self.config.hidden_layer_num)],
                                              state_is_tuple=True)

        (output_fw_seq, output_bw_seq), _ = tf.nn.bidirectional_dynamic_rnn(fw_cell, bw_cell, inputs,
                                                                            sequence_length=sequence_lengths,
                                                                            dtype=tf.float32,
                                                                            scope='dynamic_rnn_layer')
        output = tf.concat([output_fw_seq, output_bw_seq], axis=-1, name="output")

        with tf.variable_scope("logits"):
            W = tf.get_variable("W", shape=[2 * self.config.hidden_size, self.transformer.num_labels],
                                initializer=tf.contrib.layers.xavier_initializer(),
                                dtype=tf.float32)

            b = tf.get_variable("b", shape=[self.transformer.num_labels],
                                initializer=tf.zeros_initializer(),
                                dtype=tf.float32)

            shape = tf.shape(inputs)
            batch_size, time_step = shape[0], shape[1]
            output = tf.reshape(output, [-1, 2 * self.config.hidden_size])
            logits = tf.nn.xw_plus_b(output, W, b)
            logits = tf.reshape(logits, [batch_size, -1, self.transformer.num_labels])
            logits = tf.transpose(logits, (1, 0, 2), name="logits")

        with tf.variable_scope("decoded"):
            decoded, log_prob = tf.nn.ctc_beam_search_decoder(logits, sequence_lengths, merge_repeated=True)
            dense_decoded = tf.cast(tf.sparse_tensor_to_dense(decoded[0], default_value=0), tf.int32, name="dense_decoded")
        return logits, dense_decoded

    def conv(self, conv_input, k_h, k_w, c_o, s_h, s_w, name, c_i=None, bn=False, biased=True, relu=True, padding=DEFAULT_PADDING, trainable=True):
        if not c_i:
            c_i = conv_input.get_shape()[-1]
        if c_i == 1:
            conv_input = tf.expand_dims(input=conv_input, axis=3)
        convolve = lambda i, k: tf.nn.conv2d(i, k, [1, s_h, s_w, 1], padding=padding)
        with tf.variable_scope(name) as scope:
            init_weights = tf.contrib.layers.xavier_initializer()
            init_biases = tf.constant_initializer(0.0)
            kernel = tf.get_variable('weights', [k_h, k_w, c_i, c_o], initializer=init_weights, trainable=trainable,
                                     regularizer=self.l2_regularizer(self.config.weight_decay))
            if biased:
                biases = tf.get_variable('biases', [c_o], initializer=init_biases, trainable=trainable)
                conv = convolve(conv_input, kernel)
                bias = tf.nn.bias_add(conv, biases)
                if bn:
                    bn_layer = tf.contrib.layers.batch_norm(bias, scale=True,
                                                            center=True, is_training=True, scope=name)
                else:
                    bn_layer = bias
                if relu:
                    return tf.nn.relu(bn_layer)
                else:
                    return bn_layer
            else:
                conv = convolve(conv_input, kernel)
                if bn:
                    bn_layer = tf.contrib.layers.batch_norm(conv, scale=True,
                                                            center=True, is_training=True, scope=name)
                else:bn_layer = conv
                if relu:
                    return tf.nn.relu(bn_layer)
                return bn_layer

    def conv2d(self, conv_input, k_h, k_w, c_o, s_h, s_w, name, c_i=None, biased=True, relu=True, padding=DEFAULT_PADDING, trainable=True):
        if not c_i: c_i = conv_input.get_shape()[-1]
        convolve = lambda i, k: tf.nn.conv2d(i, k, [1, s_h, s_w, 1], padding=padding)
        with tf.variable_scope(name) as scope:
            init_weights = tf.contrib.layers.xavier_initializer()
            init_biases = tf.constant_initializer(0.0)
            kernel = tf.get_variable('weights', [k_h, k_w, c_i, c_o], initializer=init_weights, trainable=trainable,
                                     regularizer=self.l2_regularizer(self.config.weight_decay))
            if biased:
                biases = tf.get_variable('biases', [c_o], initializer=init_biases, trainable=trainable)
                conv = convolve(conv_input, kernel)
                if relu:
                    bias = tf.nn.bias_add(conv, biases)
                    return tf.nn.relu(bias)
                return tf.nn.bias_add(conv, biases)
            else:
                conv = convolve(conv_input, kernel)
                if relu:
                    return tf.nn.relu(conv)
                return conv

    def max_pool(self, pool_input, k_h, k_w, s_h, s_w, name, padding=DEFAULT_PADDING):
        return tf.nn.max_pool(pool_input,
                              ksize=[1, k_h, k_w, 1],
                              strides=[1, s_h, s_w, 1],
                              padding=padding,
                              name=name)

    def l2_regularizer(self, weight_decay=0.0005, scope=None):
        def regularizer(tensor):
            with tf.name_scope(scope, default_name='l2_regularizer', values=[tensor]):
                l2_weight = tf.convert_to_tensor(weight_decay,
                                       dtype=tensor.dtype.base_dtype,
                                       name='weight_decay')
                return tf.multiply(l2_weight, tf.nn.l2_loss(tensor), name='value')
        return regularizer

    def gru_cell(self):
        gru = tf.contrib.rnn.GRUCell(self.config.hidden_size)
        gru = tf.contrib.rnn.DropoutWrapper(cell=gru, input_keep_prob=self.input_keep_prob,
                                            output_keep_prob=self.output_keep_prob)
        return gru

    def save(self, output_path):
        save_graph_value_scopes = [self.scope + "logits/logits", self.scope + "decoded/dense_decoded"]
        logging.info(save_graph_value_scopes)
        graph = tf.graph_util.convert_variables_to_constants(self.session, self.session.graph_def,
                                                             save_graph_value_scopes)
        with tf.gfile.GFile(output_path + ".pb", "wb") as f:
            f.write(graph.SerializeToString())
