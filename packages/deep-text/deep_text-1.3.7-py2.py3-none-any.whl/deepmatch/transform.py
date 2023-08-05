# -*- coding=utf-8 -*-
import os
from abc import abstractmethod

import numpy as np
import tensorflow as tf
from gensim.models import word2vec
from common.transform import Transform
import logging


class MatchTransform(Transform):
    def __init__(self, config, temp_dir="runs", corpus_iter=None):
        super(MatchTransform, self).__init__(config, temp_dir, corpus_iter)

        self.doc1_queue = None
        self.doc2_queue = None
        self.label_queue = None
        self.test_doc1_data = np.array([])
        self.test_doc2_data = np.array([])
        self.test_label_data = np.array([])
        self.class_num = 0

    @abstractmethod
    def transform_docs(self, docs, front=True):
        pass

    def load_custom_data(self):
        pass

    @abstractmethod
    def parse_line(self, line):
        pass


class DeepMatchTransform(MatchTransform):
    def __init__(self, config, temp_dir="runs", corpus_iter=None):
        super(DeepMatchTransform, self).__init__(config, temp_dir, corpus_iter)

    def transform_docs(self, docs, front=True):
        doc_ids = []
        for doc in docs:
            ids = np.array([self.w2id.get(word, 0) for word in doc])
            if front:
                doc_ids.append(self.pad(ids, self.config.sequence_lengths[0], 0))
            else:
                doc_ids.append(self.pad(ids, self.config.sequence_lengths[1], 0))
        return np.array(doc_ids)

    def transform_impl(self):
        logging.info("Build tfrecord file...")

        writer = tf.python_io.TFRecordWriter(self.tfrecord_path)
        word_count = 1
        label_count = 0

        vocab_fp = open(self.vocab_path, "w")

        w2v_model = word2vec.Word2Vec.load(self.w2v_model_path)
        w2v_size = w2v_model.layer1_size

        counter = 0
        vecs = [0.0] * w2v_size
        with open(self.train_input_path, "r") as fp:
            for line in fp:
                try:
                    doc1s, doc2s, label = self.parse_line(line.strip())
                except Exception as e:
                    logging.error("Parse line error! error: {} line: {}", (e, line))
                    continue

                counter += 1
                if counter % 10000 == 0:
                    logging.info("Transform %d" % counter)

                if len(doc1s) == 0 or len(doc2s) == 0:
                    continue

                for docs in [doc1s, doc2s]:
                    for w in docs:
                        if w not in self.w2id:
                            self.w2id[w] = word_count
                            self.id2w[word_count] = w

                            v = self.get_word2vec(w2v_model, w)
                            vecs.extend(v)

                            word_count += 1
                            vocab_fp.write(w + "\n")

                doc1_words = [self.w2id[w] for w in doc1s]
                doc2_words = [self.w2id[w] for w in doc2s]
                example = tf.train.Example(features=tf.train.Features(feature={
                    'doc1': tf.train.Feature(int64_list=tf.train.Int64List(value=doc1_words)),
                    'doc2': tf.train.Feature(int64_list=tf.train.Int64List(value=doc2_words)),
                    'label': tf.train.Feature(float_list=tf.train.FloatList(value=[label])),
                }))
                writer.write(example.SerializeToString())

        self.vocab_size = word_count
        self.class_num = label_count
        self.word_vector = np.array(vecs).reshape([word_count, w2v_size])
        np.save(self.word_vector_path, self.word_vector)

        vocab_fp.flush()
        vocab_fp.close()
        writer.flush()
        writer.close()

        if os.path.exists(self.tfrecord_path):
            self.load_tfrecords_data()

        if os.path.exists(self.test_input_path):
            self.load_test_data()

    def load_tfrecords_data(self):
        logging.info("Load tfrecord data %s", self.tfrecord_path)
        filename_queue = tf.train.string_input_producer([self.tfrecord_path], num_epochs=self.config.epoch)
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(
            serialized_example,
            features={
                'doc1': tf.VarLenFeature(tf.int64),
                'doc2': tf.VarLenFeature(tf.int64),
                'label': tf.FixedLenFeature([], tf.float32),
            })

        label = features['label']
        doc1 = features['doc1']
        doc2 = features['doc2']

        doc1_q, doc2_q, label_q = tf.train.shuffle_batch([doc1, doc2, label], batch_size=self.config.batch_size,
                                                         capacity=self.config.batch_queue_capacity,
                                                         num_threads=self.config.batch_queue_thread,
                                                         min_after_dequeue=self.config.batch_min_after_dequeue)
        self.doc1_queue = doc1_q
        self.doc2_queue = doc2_q
        self.label_queue = label_q

    def load_test_data(self):
        with open(self.test_input_path, "r", errors="ignore") as fp:
            logging.info("Load test data %s" % self.test_input_path)
            docs1 = []
            docs2 = []
            lss = []
            for line in fp:
                try:
                    doc1, doc2, label = self.parse_line(line.strip())
                except Exception as e:
                    logging.error("Parse line error! error: {} line: {}", (e, line))
                    continue

                if len(doc1) == 0 or len(doc2) == 0:
                    continue

                if 0 < self.config.sequence_lengths[0] < len(doc1):
                    doc1 = doc1[:self.config.sequence_lengths[0]]
                if 0 < self.config.sequence_lengths[1] < len(doc2):
                    doc2 = doc2[:self.config.sequence_lengths[1]]
                docs1.append(doc1)
                docs2.append(doc2)
                lss.append(label)

            test_data_labels = []
            test_data_docs1 = []
            test_data_docs2 = []
            for d1, d2, l in zip(docs1, docs2, lss):
                words1 = [self.w2id.get(w, 0) for w in d1]
                words1 = self.pad(words1, self.config.sequence_lengths[0], 0)

                words2 = [self.w2id.get(w, 0) for w in d2]
                words2 = self.pad(words2, self.config.sequence_lengths[1], 0)

                test_data_labels.append(l)
                test_data_docs1.append(words1)
                test_data_docs2.append(words2)

            self.test_label_data = np.array(test_data_labels)
            self.test_doc1_data = np.array(test_data_docs1)
            self.test_doc2_data = np.array(test_data_docs2)
            logging.info("Load test data, size %d" % (self.test_label_data.shape[0]))

    def pull_batch(self, sess):
        _labels, _doc1_sparse, _doc2_sparse = sess.run([self.label_queue, self.doc1_queue, self.doc2_queue])
        _docs1 = self.sparse_to_dense(_doc1_sparse.indices, _doc1_sparse.dense_shape, _doc1_sparse.values, -1)
        _docs2 = self.sparse_to_dense(_doc2_sparse.indices, _doc2_sparse.dense_shape, _doc2_sparse.values, -1)

        labels = []
        docs1 = []
        docs2 = []
        for i in range(self.config.batch_size):
            sim = _labels[i]
            labels.append(sim)
            docs1.append(self.pad(_docs1[i], self.config.sequence_lengths[0], 0))
            docs2.append(self.pad(_docs2[i], self.config.sequence_lengths[1], 0))

        return {"doc1_batch": np.array(docs1), "doc2_batch": np.array(docs2), "label_batch": np.array(labels)}

    def get_test_data(self):
        return {"doc1_batch": self.test_doc1_data, "doc2_batch": self.test_doc2_data, "label_batch": self.test_label_data}

