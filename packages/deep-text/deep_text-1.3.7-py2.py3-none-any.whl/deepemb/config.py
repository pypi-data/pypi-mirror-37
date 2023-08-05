# -*- coding=utf-8 -*-
from common.config import BaseConfig


class SkipThoughtConfig(BaseConfig):
    def __init__(self, json_str, train_input_path, test_input_path=None):
        super(SkipThoughtConfig, self).__init__(json_str, train_input_path, test_input_path)

        self.model_name = "deepemb/skip-thought"

        self.seq_cut_length = self._config_object.get("seq_cut_length", -1)

        self.input_keep_prob = self._config_object.get("input_keep_prob", 0.8)
        self.output_keep_prob = self._config_object.get("output_keep_prob", 0.5)

        self.hidden_size = self._config_object.get("hidden_size", 20)

        self.show()

