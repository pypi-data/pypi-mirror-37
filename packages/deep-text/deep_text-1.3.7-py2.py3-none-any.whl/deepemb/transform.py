# -*- coding=utf-8 -*-
import os
from abc import abstractmethod

import numpy as np
import tensorflow as tf
from gensim.models import word2vec
from common.transform import Transform
import logging


class SkipThoughtTransform(Transform):
    def __init__(self, config, temp_dir="runs", corpus_iter=None):
        super(SkipThoughtTransform, self).__init__(config, temp_dir, corpus_iter)

        self.input_queue = None
        self.input_lens_queue = None
        self.output_prev_queue = None
        self.output_prev_lens_queue = None
        self.output_post_queue = None
        self.output_post_lens_queue = None

        self.test_input_data = np.array([])
        self.test_input_lens = np.array([])
        self.test_output_prev_data = np.array([])
        self.test_target_prev_data = np.array([])
        self.test_prev_lens = np.array([])
        self.test_prev_weights = np.array([])
        self.test_output_post_data = np.array([])
        self.test_target_post_data = np.array([])
        self.test_post_lens = np.array([])
        self.test_post_weights = np.array([])

    def load_custom_data(self):
        pass

    def load_test_data(self):
        with open(self.test_input_path, "r", errors="ignore") as fp:
            logging.info("Load test data %s" % self.test_input_path)
            input_list = []
            prev_list = []
            post_list = []
            input_max_len = 0
            prev_max_len = 0
            post_max_len = 0
            for line in fp:
                try:
                    inputs, prevs, posts = self.parse_text_line(line)
                    input_len = len(inputs)
                    prevs_len = len(prevs) - 1
                    posts_len = len(posts) - 1
                except Exception as e:
                    logging.error("Tag line error! error: {} line: {}", (e, line))
                    continue
                if input_len == 0 or prevs_len == 0 or posts_len == 0:
                    continue

                if 0 < self.config.seq_cut_length < input_len:
                    inputs = inputs[:self.config.seq_cut_length]
                if 0 < self.config.seq_cut_length < prevs_len:
                    prevs = prevs[:self.config.seq_cut_length]
                if 0 < self.config.seq_cut_length < posts_len:
                    posts = posts[:self.config.seq_cut_length]

                input_list.append(inputs)
                if input_len > self.config.seq_cut_length:
                    input_len = self.config.seq_cut_length
                if input_len > input_max_len:
                    input_max_len = input_len

                prev_list.append(prevs)
                if prevs_len > self.config.seq_cut_length:
                    prevs_len = self.config.seq_cut_length
                if prevs_len > prev_max_len:
                    prev_max_len = prevs_len

                post_list.append(posts)
                if posts_len > self.config.seq_cut_length:
                    posts_len = self.config.seq_cut_length
                if posts_len > post_max_len:
                    post_max_len = posts_len

            test_input_data = []
            test_input_lens = []
            test_output_prev_data = []
            test_target_prev_data = []
            test_prev_lens = []
            test_prev_weights = []
            test_output_post_data = []
            test_target_post_data = []
            test_post_lens = []
            test_post_weights = []
            for ins, prs, pos in zip(input_list, prev_list, post_list):
                inputs = [self.w2id.get(w, 0) for w in ins]
                prevs = [self.w2id.get(w, 0) for w in prs]
                posts = [self.w2id.get(w, 0) for w in pos]

                test_input_lens.append(len(inputs))
                test_prev_lens.append(len(prevs)-1)
                test_post_lens.append(len(posts)-1)

                prev_weight = [1.] * test_prev_lens[-1] + [0.] * (prev_max_len - test_prev_lens[-1])
                post_weight = [1.] * test_post_lens[-1] + [0.] * (post_max_len - test_post_lens[-1])
                test_prev_weights.append(prev_weight)
                test_post_weights.append(post_weight)

                inputs = self.pad(inputs, input_max_len, 0)
                prevs = self.pad(prevs[:-1], prev_max_len, 0)
                prev_targets = self.pad(prevs[1:], prev_max_len, 0)
                posts = self.pad(posts[:-1], post_max_len, 0)
                post_targets = self.pad(posts[1:], post_max_len, 0)

                test_input_data.append(inputs)

                test_output_prev_data.append(prevs)
                test_target_prev_data.append(prev_targets)

                test_output_post_data.append(posts)
                test_target_post_data.append(post_targets)

            self.test_input_data = np.array(test_input_data)
            self.test_input_lens = np.array(test_input_lens)
            self.test_output_prev_data = np.array(test_output_prev_data)
            self.test_target_prev_data = np.array(test_target_prev_data)
            self.test_prev_lens = np.array(test_prev_lens)
            self.test_prev_weights = np.array(test_prev_weights)
            self.test_output_post_data = np.array(test_output_post_data)
            self.test_target_post_data = np.array(test_target_post_data)
            self.test_post_lens = np.array(test_post_lens)
            self.test_post_weights = np.array(test_post_weights)
            logging.info("Load test data, size %d" % self.test_input_data.shape[0])

    def load_tfrecords_data(self):
        logging.info("Load tfrecord data %s", self.tfrecord_path)
        filename_queue = tf.train.string_input_producer([self.tfrecord_path], num_epochs=self.config.epoch)
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(
            serialized_example,
            features={
                'input': tf.VarLenFeature(tf.int64),
                'input_lens': tf.FixedLenFeature([], tf.int64),
                'output_prev': tf.VarLenFeature(tf.int64),
                'output_prev_lens': tf.FixedLenFeature([], tf.int64),
                'output_post': tf.VarLenFeature(tf.int64),
                'output_post_lens': tf.FixedLenFeature([], tf.int64)
            })

        input = features['input']
        input_lens = features['input_lens']

        output_prev = features['output_prev']
        output_prev_lens = features['output_prev_lens']

        output_post = features['output_post']
        output_post_lens = features['output_post_lens']

        input_q, input_lens_q,\
        output_prev_q, output_prev_lens_q,\
        output_post_q, output_post_lens_q \
            = tf.train.shuffle_batch([input, input_lens,
                                      output_prev, output_prev_lens,
                                      output_post, output_post_lens],
                                     batch_size=self.config.batch_size,
                                     capacity=self.config.batch_queue_capacity,
                                     num_threads=self.config.batch_queue_thread,
                                     min_after_dequeue=self.config.batch_min_after_dequeue)
        self.input_queue = input_q
        self.input_lens_queue = input_lens_q
        self.output_prev_queue = output_prev_q
        self.output_prev_lens_queue = output_prev_lens_q
        self.output_post_queue = output_post_q
        self.output_post_lens_queue = output_post_lens_q

    def transform_parts(self, multi_parts):
        mps = []
        max_len = max(map(lambda x: len(x), multi_parts))
        for parts in multi_parts:
            ids = np.array([self.w2id.get(p, 0) for p in parts])
            mps.append(self.pad(ids, max_len, 0))
        return np.array(mps)

    def pull_batch(self, sess):
        input_sparse, input_lens, \
        output_prev_sparse, prev_lens, \
        output_post_sparse, post_lens \
            = sess.run([self.input_queue,
                        self.input_lens_queue,
                        self.output_prev_queue,
                        self.output_prev_lens_queue,
                        self.output_post_queue,
                        self.output_post_lens_queue])

        _input = self.sparse_to_dense(input_sparse.indices, input_sparse.dense_shape, input_sparse.values, -1)
        _output_prev = self.sparse_to_dense(output_prev_sparse.indices, output_prev_sparse.dense_shape, output_prev_sparse.values, -1)
        _output_post = self.sparse_to_dense(output_post_sparse.indices, output_post_sparse.dense_shape, output_post_sparse.values, -1)

        if self.config.seq_cut_length > 0:
            input_lens[np.where(input_lens > self.config.seq_cut_length)] = self.config.seq_cut_length
            prev_lens[np.where(prev_lens > self.config.seq_cut_length)] = self.config.seq_cut_length
            post_lens[np.where(post_lens > self.config.seq_cut_length)] = self.config.seq_cut_length

        input_max_len = max(input_lens)
        prev_max_len = max(prev_lens)
        post_max_len = max(post_lens)

        inputs = []
        output_prevs = []
        target_prevs = []
        prev_weights = []
        output_posts = []
        target_posts = []
        post_weights = []
        for i in range(self.config.batch_size):
            inputs.append(self.pad(_input[i], input_max_len, 0))
            output_prevs.append(self.pad(_output_prev[i][:-1], prev_max_len, 0))
            target_prevs.append(self.pad(_output_prev[i][1:], prev_max_len, 0))
            output_posts.append(self.pad(_output_post[i][:-1], post_max_len, 0))
            target_posts.append(self.pad(_output_post[i][1:], post_max_len, 0))
            prev_weights.append([1.] * prev_lens[i] + [0.] * (prev_max_len - prev_lens[i]))
            post_weights.append([1.] * post_lens[i] + [0.] * (post_max_len - post_lens[i]))

        return {"inputs": np.array(inputs),
                "input_lens": input_lens,
                "output_prevs": np.array(output_prevs),
                "target_prevs": np.array(target_prevs),
                "prev_lens": prev_lens,
                "prev_weights": prev_weights,
                "output_posts": np.array(output_posts),
                "target_posts": np.array(target_posts),
                "output_post_lens": post_lens,
                "post_weights": post_weights}

    def get_test_data(self):
        return {"inputs": self.test_input_data,
                "input_lens": self.test_input_lens,
                "output_prevs": self.test_output_prev_data,
                "target_prevs": self.test_target_prev_data,
                "prev_lens": self.test_prev_lens,
                "prev_weights": self.test_prev_weights,
                "output_posts": self.test_output_post_data,
                "target_posts": self.test_target_post_data,
                "output_post_lens": self.test_post_lens,
                "post_weights": self.test_post_weights}

    def transform_impl(self):
        logging.info("Build tfrecord file...")
        
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
            
        writer = tf.python_io.TFRecordWriter(self.tfrecord_path)
        word_count = 1  # 0 is UNK

        vocab_fp = open(self.vocab_path, "w")
        w2v_model = word2vec.Word2Vec.load(self.w2v_model_path)
        w2v_layer_size = w2v_model.layer1_size

        counter = 0
        vecs = [0.0] * w2v_layer_size
        with open(self.train_input_path, "r", errors="ignore") as fp:
            for line in fp:
                line = line.strip()
                try:
                    inputs, prevs, posts = self.parse_text_line(line)
                except Exception as e:
                    logging.error("Parse text line error! error: {} line: {}", (e, line))
                    continue

                counter += 1
                if counter % 10000 == 0:
                    logging.info("Transform %d" % counter)

                input_len = len(inputs)
                prevs_len = len(prevs) - 1
                posts_len = len(posts) - 1
                if input_len == 0 or prevs_len == 0 or posts_len == 0:
                    continue

                for s in [inputs, prevs, posts]:
                    for w in s:
                        if w not in self.w2id:
                            self.w2id[w] = word_count
                            self.id2w[word_count] = w

                            v = self.get_word2vec(w2v_model, w)
                            vecs.extend(v)

                            word_count += 1
                            vocab_fp.write(w + "\n")

                input_ids = [self.w2id.get(w, 0) for w in inputs]
                prev_ids = [self.w2id.get(w, 0) for w in prevs]
                post_ids = [self.w2id.get(w, 0) for w in posts]
                example = tf.train.Example(features=tf.train.Features(feature={
                    'input': tf.train.Feature(int64_list=tf.train.Int64List(value=input_ids)),
                    'input_lens': tf.train.Feature(int64_list=tf.train.Int64List(value=[input_len])),
                    'output_prev': tf.train.Feature(int64_list=tf.train.Int64List(value=prev_ids)),
                    'output_prev_lens': tf.train.Feature(int64_list=tf.train.Int64List(value=[prevs_len])),
                    'output_post': tf.train.Feature(int64_list=tf.train.Int64List(value=post_ids)),
                    'output_post_lens': tf.train.Feature(int64_list=tf.train.Int64List(value=[posts_len]))
                }))
                writer.write(example.SerializeToString())

        self.vocab_size = word_count
        self.word_vector = np.array(vecs).reshape([word_count, w2v_layer_size])
        np.save(self.word_vector_path, self.word_vector)

        vocab_fp.close()
        writer.close()

        if os.path.exists(self.tfrecord_path):
            self.load_tfrecords_data()
        
        if os.path.exists(self.test_input_path):
            self.load_test_data()
            
    @abstractmethod
    def parse_text_line(self, line):
        pass

