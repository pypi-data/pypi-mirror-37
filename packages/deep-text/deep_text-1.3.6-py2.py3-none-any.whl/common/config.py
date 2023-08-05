# -*- coding=utf-8 -*-
import os
import json
import multiprocessing
from .embedding_types import EmbeddingType
import logging


class Config(object):
    def __init__(self, json_str):
        self._config_object = json.loads(json_str)

    def show(self):
        for attr, value in sorted(self.__dict__.items()):
            if attr == "_config_object":
                continue
            logging.debug("{}={}".format(attr.upper(), value))
        logging.debug("")

    def dump(self, path):
        obj = {}
        for attr, value in sorted(self.__dict__.items()):
            if attr == "_config_object" or attr == "test_input_path" or attr == "train_input_path":
                continue
            obj[attr] = value
        json_str = json.dumps(obj, indent=4)
        with open(path, "w") as fp:
            fp.write(json_str)


class BaseConfig(Config):
    def __init__(self, json_str, train_input_path, test_input_path=None, default_embedding=EmbeddingType.word2vec):
        super(BaseConfig, self).__init__(json_str)
        self.train_input_path = train_input_path
        self.test_input_path = test_input_path

        self.model_name = None
        self.temp_path = self._config_object.get("temp_path", "")

        self.lr = self._config_object.get("lr", 0.0001)
        self.epoch = self._config_object.get("epoch", 5)
        self.batch_size = self._config_object.get("batch_size", 64)
        self.gradient_clip = self._config_object.get("gradient_clip", 0.5)

        self.evaluate_every = self._config_object.get("evaluate_every", 1000)
        self.checkpoint_every = self._config_object.get("checkpoint_every", 1000)
        self.num_checkpoints = self._config_object.get("num_checkpoints", 5)

        self.allow_soft_placement = self._config_object.get("allow_soft_placement", True)
        self.log_device_placement = self._config_object.get("log_device_placement", False)
        self.cpu_count = self._config_object.get("cpu_count", multiprocessing.cpu_count())

        self.cuda_visable_devices = self._config_object.get("cuda_visable_devices", "0")

        self.gpu_list = self._config_object.get("gpu_list", [])
        if len(self.gpu_list) > 0:
            self.cuda_visable_devices = ",".join([str(g) for g in self.gpu_list])

        os.environ["CUDA_VISIBLE_DEVICES"] = self.cuda_visable_devices

        self.embedding_type = default_embedding

        if default_embedding == EmbeddingType.empty:
            self.embedding_size = self._config_object.get("embedding_size", 128)
        if default_embedding == EmbeddingType.custom:
            self.embedding_size = self._config_object.get("embedding_size", 128)
            self.custom_embedding_file = self._config_object.get("custom_embedding_file", "")
        elif default_embedding == EmbeddingType.word2vec:
            # config for word2vec train
            self.embedding_size = self._config_object.get("embedding_size", 128)
            self.w2v_alpha = self._config_object.get("w2v_alpha", 0.025)
            self.w2v_window = self._config_object.get("w2v_window", 5)
            self.w2v_min_count = self._config_object.get("w2v_min_count", 3)
            self.w2v_sample = self._config_object.get("w2v_sample", 0.001)
            self.w2v_workers = self._config_object.get("w2v_workers", self.cpu_count)
            self.w2v_negative = self._config_object.get("w2v_negative", 5)
            self.w2v_iter_times = self._config_object.get("w2v_iter_times", 5)

        # batch config
        self.batch_queue_thread = self._config_object.get("batch_queue_thread", self.cpu_count)
        self.batch_queue_capacity = self._config_object.get("batch_queue_capacity", 500000)
        self.batch_min_after_dequeue = self._config_object.get("batch_min_after_dequeue", 100000)

