# -*- coding=utf-8 -*-
import os
from abc import abstractmethod

import numpy as np
import tensorflow as tf
from gensim.models import word2vec
from common.transform import Transform
import logging


class DeepLMTransform(Transform):
    def __init__(self, config, temp_dir="runs", corpus_iter=None):
        super(DeepLMTransform, self).__init__(config, temp_dir, corpus_iter)

        self.text_queue = None
        self.seq_lens_queue = None
        self.test_text_data = np.array([])
        self.test_label_data = np.array([])
        self.test_lengths = np.array([])
        self.test_weights = np.array([])
        self.lm_start_label = "<LM_START_LABEL>"
        self.lm_end_label = "<LM_END_LABEL>"

    def load_custom_data(self):
        pass

    def load_test_data(self):
        with open(self.test_input_path, "r", errors="ignore") as fp:
            logging.info("Load test data %s" % self.test_input_path)
            wss = []
            max_len = 0
            for line in fp:
                try:
                    ws = self.parse_text_line(line)
                    wslen = len(ws) - 1
                except Exception as e:
                    logging.error("Tag line error! error: {} line: {}", (e, line))
                    continue
                if ws is None or wslen == 0:
                    continue
                if 0 < self.config.seq_cut_length < wslen:
                    ws = ws[:self.config.seq_cut_length]
                wss.append(ws)
                if wslen > self.config.seq_cut_length:
                    wslen = self.config.seq_cut_length
                if wslen > max_len:
                    max_len = wslen

            test_data_text = []
            test_data_label = []
            test_data_leng = []
            test_data_weight = []
            for ws in wss:
                words = [self.w2id.get(w, 0) for w in ws]

                words = self.pad(words[:-1], max_len, 0)
                labels = self.pad(words[1:], max_len, 0)
                test_data_text.append(words)
                test_data_label.append(labels)
                test_data_leng.append(len(words))

                size = len(words)
                weight = [1.] * max_len
                for i in range(max_len):
                    if i >= size:
                        weight[i] = 0.
                test_data_weight.append(weight)

            self.test_text_data = np.array(test_data_text)
            self.test_label_data = np.array(test_data_label)
            self.test_lengths = np.array(test_data_leng)
            self.test_weights = np.array(test_data_weight)
            logging.info("Load test data, size %d,%d" % (self.test_text_data.shape[0],self.test_text_data.shape[1]))
         
    def load_tfrecords_data(self):
        logging.info("Load tfrecord data %s", self.tfrecord_path)
        filename_queue = tf.train.string_input_producer([self.tfrecord_path], num_epochs=self.config.epoch)
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(
            serialized_example,
            features={
                'text': tf.VarLenFeature(tf.int64),
                'seq_lens': tf.FixedLenFeature([], tf.int64)
            })

        text = features['text']
        seq_lens = features['seq_lens']

        text_q, seq_lens_q = tf.train.shuffle_batch([text, seq_lens], batch_size=self.config.batch_size,
                                                    capacity=self.config.batch_queue_capacity,
                                                    num_threads=self.config.batch_queue_thread,
                                                    min_after_dequeue=self.config.batch_min_after_dequeue)
        self.text_queue = text_q
        self.seq_lens_queue = seq_lens_q

    def transform_parts(self, multi_parts):
        mps = []
        max_len = max(map(lambda x: len(x), multi_parts)) + 2 # 2 for pad
        for parts in multi_parts:
            pad_parts = [self.lm_start_label]
            pad_parts.extend(parts)
            pad_parts.append(self.lm_end_label)
            ids = np.array([self.w2id.get(p, 0) for p in pad_parts])
            mps.append(self.pad(ids, max_len, 0))
        return np.array(mps)

    def pull_batch(self, sess):
        _text_sparse, _seq_lens = sess.run([self.text_queue, self.seq_lens_queue])
        _texts = self.sparse_to_dense(_text_sparse.indices, _text_sparse.dense_shape, _text_sparse.values, -1)

        if self.config.seq_cut_length > 0:
            _seq_lens[np.where(_seq_lens > self.config.seq_cut_length)] = self.config.seq_cut_length

        _seq_lens = _seq_lens - 1
        max_len = max(_seq_lens)

        labels = []
        texts = []
        weights = []
        for i in range(self.config.batch_size):
            doc = _texts[i][:-1]
            label = _texts[i][1:]
            size = len(doc)
            weight = [1.] * max_len
            for i in range(len(weight)):
                if i >= size:
                    weight[i] = 0.
            texts.append(self.pad(doc, max_len, 0))
            labels.append(self.pad(label, max_len, 0))
            weights.append(weight)

        return {"label_batch": np.array(labels),
                "doc_batch": np.array(texts),
                "seq_lens": _seq_lens,
                "weights": np.array(weights)}
    
    def get_test_data(self):
        return {"label_batch": self.test_label_data,
                "doc_batch": self.test_text_data,
                "seq_lens": self.test_lengths,
                "weights": self.test_weights}

    def transform_impl(self):
        logging.info("Build tfrecord file...")
        
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
            
        writer = tf.python_io.TFRecordWriter(self.tfrecord_path)
        word_count = 1  # 0 is UNK

        vocab_fp = open(self.vocab_path, "w")

        counter = 0
        with open(self.train_input_path, "r", errors="ignore") as fp:
            for line in fp:
                line = line.strip()
                try:
                    ws = self.parse_text_line(line)
                except Exception as e:
                    logging.error("Parse text line error! error: {} line: {}", (e, line))
                    continue

                counter += 1
                if counter % 10000 == 0:
                    logging.info("Transform %d" % counter)
                    
                if ws is None or len(ws) == 0:
                    continue

                for w in ws:
                    if w not in self.w2id:
                        self.w2id[w] = word_count
                        self.id2w[word_count] = w

                        word_count += 1
                        vocab_fp.write(w + "\n")

                words = [self.w2id[w] for w in ws]
                example = tf.train.Example(features=tf.train.Features(feature={
                    'text': tf.train.Feature(int64_list=tf.train.Int64List(value=words)),
                    'seq_lens': tf.train.Feature(int64_list=tf.train.Int64List(value=[len(words)-1]))
                }))
                writer.write(example.SerializeToString())

        self.vocab_size = word_count

        vocab_fp.close()
        writer.close()

        if os.path.exists(self.tfrecord_path):
            self.load_tfrecords_data()
        
        if os.path.exists(self.test_input_path):
            self.load_test_data()
            
    @abstractmethod
    def parse_text_line(self, line):
        pass

