# -*- coding=utf-8 -*-
from common.config import BaseConfig


class DeepOCRConfig(BaseConfig):
    def __init__(self, json_str, train_input_path, test_input_path=None):
        super(DeepOCRConfig, self).__init__(json_str, train_input_path, test_input_path)

        self.model_name = "deepocr/cnn-lstm-ctc"

        self.weight_decay = self._config_object.get("weight_decay", 0.0005)
        self.n_channels = self._config_object.get("n_channels", 3)
        self.image_shape = self._config_object.get("image_shape", [320, 64])
        self.sequence_length = self._config_object.get("sequence_length", 237)

        self.input_keep_prob = self._config_object.get("input_keep_prob", 0.8)
        self.output_keep_prob = self._config_object.get("output_keep_prob", 0.5)

        self.hidden_size = self._config_object.get("hidden_size", 20)
        self.hidden_layer_num = self._config_object.get("hidden_layer_num", 1)

        self.show()

