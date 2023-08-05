# -*- coding=utf-8 -*-
from common.embedding_types import EmbeddingType
from .model import DeepMatchModel
import tensorflow as tf
import logging
from tensorflow.contrib.tensorboard.plugins import projector


class CDSSM(DeepMatchModel):
    def __init__(self, session, transformer, config, multi_gpu_trainer=False):
        super(CDSSM, self).__init__(session, transformer, config, multi_gpu_trainer)
        self.input_doc1 = tf.placeholder(tf.int64, shape=[None, config.sequence_lengths[0]], name="input_doc1")
        self.input_doc2 = tf.placeholder(tf.int64, shape=[None, config.sequence_lengths[1]], name="input_doc2")
        self.labels = tf.placeholder(tf.float32, shape=[None], name="input_label")  # 0.0 ~ 1.0
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
                logging.info("Embbeding fill data %s" % self.W.name)
            self.W = tf.get_variable("w", shape=[transformer.vocab_size, config.embedding_size],
                                     initializer=embedding_initializer,
                                     dtype=tf.float32)
            embedded_doc1 = tf.nn.embedding_lookup(self.W, self.input_doc1)
            embedded_doc2 = tf.nn.embedding_lookup(self.W, self.input_doc2)

            self.embedded_chars_doc1 = tf.nn.dropout(embedded_doc1, self.input_keep_prob,
                                                     [self.batch_size, config.sequence_lengths[0], 1],
                                                     seed=3, name="input_dorpout_doc1")
            self.embedded_chars_doc2 = tf.nn.dropout(embedded_doc2, self.input_keep_prob,
                                                     [self.batch_size, config.sequence_lengths[1], 1],
                                                     seed=3, name="input_dorpout_doc2")

        self.embedded_chars_doc1_expanded = tf.expand_dims(self.embedded_chars_doc1, -1)
        self.embedded_chars_doc2_expanded = tf.expand_dims(self.embedded_chars_doc2, -1)

        # create dnn layer
        with tf.variable_scope('cnn_doc1'):
            # Create a convolution + maxpool layer for each filter size
            pooled_outputs = []
            for i, filter_size in enumerate(config.filter_sizes[0]):
                with tf.name_scope("conv-maxpool-%s" % filter_size):
                    # Convolution Layer
                    filter_shape = [filter_size, self.config.embedding_size, 1, config.num_filters]
                    W = tf.get_variable("W_%s" % filter_size, shape=filter_shape, initializer=tf.truncated_normal_initializer(stddev=0.1))
                    b = tf.get_variable("b_%s" % filter_size, shape=[config.num_filters], initializer=tf.constant_initializer(0.1, tf.float32))
                    conv = tf.nn.conv2d(
                        self.embedded_chars_doc1_expanded,
                        W,
                        strides=[1, 1, 1, 1],
                        padding="VALID",
                        name="conv")
                    # Apply nonlinearity
                    h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                    # Maxpooling over the outputs
                    pooled = tf.nn.max_pool(
                        h,
                        ksize=[1, self.config.sequence_lengths[0] - filter_size + 1, 1, 1],
                        strides=[1, 1, 1, 1],
                        padding='VALID',
                        name="pool")
                pooled_outputs.append(pooled)

            # Combine all the pooled features
            num_filters_total = config.num_filters * len(config.filter_sizes[0])
            h_pool = tf.concat(pooled_outputs, 3)
            h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])
            h_drop = tf.nn.dropout(h_pool_flat, self.output_keep_prob)

            W = tf.get_variable("W_fc",shape=[num_filters_total, config.sent_vector_size],
                                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.get_variable("b_fc", shape=[config.sent_vector_size], initializer=tf.constant_initializer(0.1))
            self.doc1_vector = tf.nn.xw_plus_b(h_drop, W, b, name="doc_vector")

        with tf.variable_scope('cnn_doc2'):
            # Create a convolution + maxpool layer for each filter size
            pooled_outputs = []
            for i, filter_size in enumerate(config.filter_sizes[1]):
                with tf.name_scope("conv-maxpool-%s" % filter_size):
                    # Convolution Layer
                    filter_shape = [filter_size, self.config.embedding_size, 1, config.num_filters]
                    W = tf.get_variable("W_%s" % filter_size, shape=filter_shape, initializer=tf.truncated_normal_initializer(stddev=0.1))
                    b = tf.get_variable("b_%s" % filter_size, shape=[config.num_filters], initializer=tf.constant_initializer(0.1, tf.float32))
                    conv = tf.nn.conv2d(
                        self.embedded_chars_doc2_expanded,
                        W,
                        strides=[1, 1, 1, 1],
                        padding="VALID",
                        name="conv")
                    # Apply nonlinearity
                    h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                    # Maxpooling over the outputs
                    pooled = tf.nn.max_pool(
                        h,
                        ksize=[1, self.config.sequence_lengths[1] - filter_size + 1, 1, 1],
                        strides=[1, 1, 1, 1],
                        padding='VALID',
                        name="pool")
                pooled_outputs.append(pooled)

            # Combine all the pooled features
            num_filters_total = config.num_filters * len(config.filter_sizes[1])
            h_pool = tf.concat(pooled_outputs, 3)
            h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])
            h_drop = tf.nn.dropout(h_pool_flat, self.output_keep_prob)

            W = tf.get_variable("W_fc",shape=[num_filters_total, config.sent_vector_size],
                                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.get_variable("b_fc", shape=[config.sent_vector_size], initializer=tf.constant_initializer(0.1))
            self.doc2_vector = tf.nn.xw_plus_b(h_drop, W, b, name="doc_vector")

        with tf.variable_scope('output'):
            norms1 = tf.sqrt(tf.reduce_sum(tf.square(self.doc1_vector), 1, keep_dims=False))
            norms2 = tf.sqrt(tf.reduce_sum(tf.square(self.doc2_vector), 1, keep_dims=False))
            dot = tf.reduce_sum(self.doc1_vector * self.doc2_vector, 1)
            cos_dis = tf.divide(dot, (norms1 * norms2))
            self.similarity = tf.divide((cos_dis + 1.0), 2.0, name="similarity")

        with tf.name_scope("loss"):
            self.loss = tf.reduce_sum(tf.losses.log_loss(self.labels, self.similarity), name="loss")

        with tf.name_scope("auc"):
            _, self.auc = tf.metrics.auc(self.labels, self.similarity, name="auc")

    def apply_embedding_visuel(self, summary_writer):
        config = projector.ProjectorConfig()

        embedding = config.embeddings.add()
        embedding.tensor_name = self.W.name
        embedding.metadata_path = 'embedding'

        projector.visualize_embeddings(summary_writer, config)

    def save(self, output_path):
        save_graph_value_scopes = [self.scope+"output/similarity"]
        logging.info(save_graph_value_scopes)
        graph = tf.graph_util.convert_variables_to_constants(self.session, self.session.graph_def, save_graph_value_scopes)
        with tf.gfile.GFile(output_path+".pb", "wb") as f:
            f.write(graph.SerializeToString())

