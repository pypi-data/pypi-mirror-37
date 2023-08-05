# -*- coding=utf-8 -*-
import os
from abc import abstractmethod

import numpy as np
import tensorflow as tf
from gensim.models import word2vec
from common.transform import Transform
import logging


class DeepOCRTransform(Transform):
    def __init__(self, config, temp_dir="runs", corpus_iter=None):
        super(DeepOCRTransform, self).__init__(config, temp_dir, corpus_iter)

        self.label_path = self.data_path + "/labels.txt"

        self.label2id = {}
        self.id2label = {}
        self.label_len_queue = None
        self.image_raw_queue = None
        self.label_queue = None

        self.test_label_len_data = None
        self.test_image_raw_data = None
        self.test_label_data = None

        self.num_labels = 0

    def load_custom_data(self):
        if not os.path.exists(self.label_path):
            return
        
        count = 0
        with open(self.label_path, 'r') as fp:
            for line in fp:
                line = line.replace("\n", "")
                self.id2label[count] = line
                self.label2id[line] = count
                count += 1
        self.num_labels = count
        logging.info("Load labels data, size %d" % self.num_labels)

    def load_test_data(self):
        with open(self.test_input_path, "r", errors="ignore") as fp:
            logging.info("Load test data %s" % self.test_input_path)
            label_list = []
            image_raw_data = []
            label_len_data = []
            for line in fp:
                line = line.strip()
                try:
                    image, labels = self.image_label_load(line)
                except Exception as e:
                    logging.error("Image load error! error: {} line: {}", (e, line))
                    continue

                if image is None or len(labels) == 0:
                    continue

                labels = [self.label2id[t] for t in labels]
                image_raw = image.reshape((self.config.image_shape[0], self.config.image_shape[1], -1))
                image_raw_data.append(image_raw)
                label_len_data.append(len(labels))
                label_list.append(labels)

            label_data = []
            for labels in label_list:
                label_data.extend(labels)
            self.test_image_raw_data = np.array(image_raw_data)
            self.test_label_data = np.array(label_data)
            self.test_label_len_data = np.array(label_len_data)

        logging.info("Load test data, size %d" % (self.test_image_raw_data.shape[0]))

    def load_tfrecords_data(self):
        logging.info("Load tfrecord data %s", self.tfrecord_path)
        filename_queue = tf.train.string_input_producer([self.tfrecord_path], num_epochs=self.config.epoch)
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)

        features = tf.parse_single_example(
            serialized_example,
            features={
                'label_len': tf.FixedLenFeature([], tf.int64),
                'image_raw': tf.FixedLenFeature([], tf.string),
                'label': tf.VarLenFeature(tf.int64),
            })

        label_len = features['label_len']
        image_raw = features['image_raw']
        label = features['label']

        label_len_q, image_raw_q, label_q = \
            tf.train.shuffle_batch([label_len, image_raw, label],
                                   batch_size=self.config.batch_size,
                                   capacity=self.config.batch_queue_capacity,
                                   num_threads=self.config.batch_queue_thread,
                                   min_after_dequeue=self.config.batch_min_after_dequeue)
        self.label_len_queue = label_len_q
        self.image_raw_queue = image_raw_q
        self.label_queue = label_q

    def transform_labels(self, multi_labels):
        label_ret = []
        for labels in multi_labels:
            label_ret.append([self.id2label.get(l, 0) for l in labels if (l != 0)])
        return label_ret

    def image_raw_convert(self, image_raws):
        images = []
        for image_string in image_raws:
            img_1d = np.fromstring(image_string, dtype=np.uint8)
            img = img_1d.reshape((self.config.image_shape[0], self.config.image_shape[1], -1))
            images.append(img)
        return np.array(images)

    def pull_batch(self, sess):
        _label_len, _image_raws, _label_sparse = \
            sess.run([
                self.label_len_queue,
                self.image_raw_queue,
                self.label_queue,
            ])

        _labels = self.sparse_to_dense(_label_sparse.indices, _label_sparse.dense_shape, _label_sparse.values, -1)

        labels = []
        for i in range(self.config.batch_size):
            labels.extend(_labels[i][:_label_len[i]])

        images = self.image_raw_convert(_image_raws)
        time_steps = [self.config.sequence_length] * len(images)
        return {"label_len": _label_len, "time_step": np.array(time_steps), "images": images, "labels": np.array(labels)}

    def get_test_data(self):
        time_steps = [self.config.sequence_length] * len(self.test_image_raw_data)
        return {"label_len": self.test_label_len_data,
                "time_step": np.array(time_steps),
                "images": self.test_image_raw_data,
                "labels": self.test_label_data}

    def transform_impl(self):
        logging.info("Build tfrecord file...")
        
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
            
        writer = tf.python_io.TFRecordWriter(self.tfrecord_path)

        self.label2id["BLANK"] = 0
        self.id2label[0] = "BLANK"
        label_count = 1

        label_fp = open(self.label_path, "w")

        counter = 0
        with open(self.train_input_path, "r", errors="ignore") as fp:
            for line in fp:
                line = line.strip()
                try:
                    image, labels = self.image_label_load(line)
                except Exception as e:
                    logging.error("Image load error! error: {} line: {}", (e, line))
                    continue

                counter += 1
                if counter % 10000 == 0:
                    logging.info("Transform %d" % counter)
                    
                if image is None or len(labels) == 0:
                    continue

                for l in labels:
                    if l not in self.label2id:
                        self.label2id[l] = label_count
                        self.id2label[label_count] = l
                        label_count += 1
                        label_fp.write(l + "\n")

                labels = [self.label2id[t] for t in labels]
                image_raw = image.tostring()
                features = tf.train.Features(feature={
                    'label_len': tf.train.Feature(int64_list=tf.train.Int64List(value=[len(labels)])),
                    'image_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_raw])),
                    'label': tf.train.Feature(int64_list=tf.train.Int64List(value=labels))
                    })

                example = tf.train.Example(features=features)
                writer.write(example.SerializeToString())

        self.num_labels = label_count
        label_fp.close()
        writer.close()

        if os.path.exists(self.tfrecord_path):
            self.load_tfrecords_data()
        
        if os.path.exists(self.test_input_path):
            self.load_test_data()
            
    @abstractmethod
    def image_label_load(self, line):
        pass

