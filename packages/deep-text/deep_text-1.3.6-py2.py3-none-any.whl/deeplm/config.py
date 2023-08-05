# -*- coding=utf-8 -*-
from common.config import BaseConfig
from common.embedding_types import EmbeddingType


class DeepLMConfig(BaseConfig):
    def __init__(self, json_str, train_input_path, test_input_path=None):
        super(DeepLMConfig, self).__init__(json_str, train_input_path, test_input_path,
                                           default_embedding=EmbeddingType.empty)
        self.model_name = "deeplm/deeplm"

        self.seq_cut_length = self._config_object.get("seq_cut_length", -1)

        self.input_keep_prob = self._config_object.get("input_keep_prob", 0.8)
        self.output_keep_prob = self._config_object.get("output_keep_prob", 0.5)

        self.hidden_size = self._config_object.get("hidden_size", 20)
        self.hidden_layer_num = self._config_object.get("hidden_layer_num", 1)

        self.show()

