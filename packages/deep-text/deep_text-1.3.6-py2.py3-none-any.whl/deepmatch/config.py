# -*- coding=utf-8 -*-
from common.config import BaseConfig


class CDSSMConfig(BaseConfig):
    def __init__(self, json_str, train_input_path, test_input_path=None):
        super(CDSSMConfig, self).__init__(json_str, train_input_path, test_input_path)

        self.model_name = "deepmatch/cdssm"

        self.sequence_lengths = self._config_object.get("sequence_lengths", [50, 50])
        self.num_filters = self._config_object.get("num_filters", 128)
        self.filter_sizes = self._config_object.get("filter_sizes", [[3, 4, 5], [3, 4, 5]])
        self.sent_vector_size = self._config_object.get("sent_vector_size", 128)

        self.input_keep_prob = self._config_object.get("input_keep_prob", 0.8)
        self.output_keep_prob = self._config_object.get("output_keep_prob", 0.5)

        self.show()

