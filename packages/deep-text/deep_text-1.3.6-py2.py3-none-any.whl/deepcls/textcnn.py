# -*- coding=utf-8 -*-
from abc import abstractmethod

import tensorflow as tf
import logging
from tensorflow.contrib.tensorboard.plugins import projector
from common.model import BaseModel
from common.embedding_types import EmbeddingType


class TextCNNBase(BaseModel):
    def __init__(self, session, transformer, config):
        super(TextCNNBase, self).__init__(session, transformer, config)

        self.input = tf.placeholder(tf.int32, [None, config.sequence_length], name="input")
        self.target = tf.placeholder(tf.int32, [None, transformer.class_num], name="target")
        self.batch_size = tf.placeholder(tf.int32, name="batch_size")
        self.input_keep_prob = tf.placeholder(tf.float32, name="input_keep_prob")
        self.output_keep_prob = tf.placeholder(tf.float32, name="output_keep_prob")

        # Embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            if self.config.embedding_type == EmbeddingType.word2vec:
                logging.info("Init embedding with word vector. (%d,%d)",
                             transformer.word_vector.shape[0], transformer.word_vector.shape[1])
                embedding_initializer = tf.constant_initializer(transformer.word_vector)
            else:
                logging.info("Init embedding with xavier initializer.")
                embedding_initializer = tf.contrib.layers.xavier_initializer()
            self._W = tf.get_variable("W", [transformer.vocab_size, config.embedding_size], dtype=tf.float32,
                                      initializer=embedding_initializer)
            embedded = tf.nn.embedding_lookup(self._W, self.input)
            self.embedded_chars = tf.nn.dropout(embedded, self.input_keep_prob,
                                                [self.batch_size, config.sequence_length, 1], seed=3,
                                                name="input_dorpout")

        self.embedded_chars_expanded = tf.expand_dims(self.embedded_chars, -1)

        pooled_outputs = []
        # create dnn layer
        with tf.variable_scope('cnn_layer'):
            # Create a convolution + maxpool layer for each filter size
            for i, filter_size in enumerate(config.filter_sizes):
                with tf.name_scope("conv-maxpool-%s" % filter_size):
                    # Convolution Layer
                    filter_shape = [filter_size, config.embedding_size, 1, config.num_filters]
                    W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                    b = tf.Variable(tf.constant(0.1, shape=[config.num_filters]), name="b")
                    conv = tf.nn.conv2d(
                        self.embedded_chars_expanded,
                        W,
                        strides=[1, 1, 1, 1],
                        padding="VALID",
                        name="conv")
                    # Apply nonlinearity
                    h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                    # Maxpooling over the outputs
                    pooled = tf.nn.max_pool(
                        h,
                        ksize=[1, config.sequence_length - filter_size + 1, 1, 1],
                        strides=[1, 1, 1, 1],
                        padding='VALID',
                        name="pool")
                pooled_outputs.append(pooled)

        # Combine all the pooled features
        num_filters_total = config.num_filters * len(config.filter_sizes)
        h_pool = tf.concat(pooled_outputs, 3)
        h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])
        h_drop = tf.nn.dropout(h_pool_flat, self.output_keep_prob)

        self.probs, self.loss = self.cost(h_drop, num_filters_total)

        with tf.name_scope("accuracy"):
            self.prediction = tf.argmax(self.probs, 1, name="predict")
            correct_prediction = tf.equal(self.prediction, tf.argmax(self.target, 1))
            self.correct_num = tf.reduce_sum(tf.cast(correct_prediction, tf.float32))
            self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

    @abstractmethod
    def cost(self, output, num_filters_total):
        pass

    def apply_embedding_visuel(self, summary_writer):
        config = projector.ProjectorConfig()
        embedding = config.embeddings.add()
        embedding.tensor_name = self._W.name
        embedding.metadata_path = 'embedding.csv'
        projector.visualize_embeddings(summary_writer, config)

    def save(self, output_path):
        scopes = [self.scope+"accuracy/predict"]
        graph = tf.graph_util.convert_variables_to_constants(self.session, self.session.graph_def, scopes)
        with tf.gfile.GFile(output_path+".pb", "wb") as f:
            f.write(graph.SerializeToString())


class TextCNN(TextCNNBase):
    def __init__(self, session, transformer, config):
        super(TextCNN, self).__init__(session, transformer, config)

    def cost(self, output, num_filters_total):
        with tf.variable_scope('softmax_layer'):
            softmax_w = tf.get_variable("softmax_w", shape=[num_filters_total, self.transformer.class_num],
                                        initializer=tf.contrib.layers.xavier_initializer())
            softmax_b = tf.Variable(tf.constant(0.1, shape=[self.transformer.class_num]), name="softmax_b")
            logits = tf.add(tf.matmul(output, softmax_w), softmax_b, name="logits")
            probs = tf.nn.softmax(logits, name="probs")

        with tf.name_scope("loss"):
            cross_entropy_loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits + 1e-10, labels=self.target)
            loss = tf.reduce_mean(cross_entropy_loss)
        return probs, loss


class TextCNN_M(TextCNNBase):
    def __init__(self, session, transformer, config):
        super(TextCNN_M, self).__init__(session, transformer, config)

    def cost(self, output, num_filters_total):
        with tf.variable_scope('softmax_layer'):
            softmax_w = tf.get_variable("softmax_w", shape=[num_filters_total, self.transformer.class_num],
                                        initializer=tf.contrib.layers.xavier_initializer())
            softmax_b = tf.Variable(tf.constant(0.1, shape=[self.transformer.class_num]), name="softmax_b")
            logits = tf.add(tf.matmul(output, softmax_w), softmax_b, name="logits")
            probs = tf.nn.sigmoid(logits, name="probs")

        with tf.name_scope("loss"):
            sig_loss = tf.nn.sigmoid_cross_entropy_with_logits(logits=logits,
                                                               labels=tf.cast(self.target, tf.float32))
            loss = tf.reduce_mean(tf.reduce_sum(sig_loss, axis=1))
        return probs, loss

