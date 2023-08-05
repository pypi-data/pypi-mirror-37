from deepcls.config import TextCNNConfig
from deepcls.config import TextRNNConfig
from deepcrf.config import DeepCRFConfig
from deeplm.config import DeepLMConfig
from deepmatch.config import CDSSMConfig
from deepemb.config import SkipThoughtConfig
from deepocr.config import DeepOCRConfig
import json


def load_config(path, train_input_path=None, test_input_path=None):
    with open(path, "r") as fp:
        json_str = fp.read()
        json_obj = json.loads(json_str)
        model_name = json_obj["model_name"]

    if model_name == "deepcrf/deepcrf":
        return load_deep_crf_config(path, train_input_path, test_input_path)
    elif model_name == "deeplm/deeplm":
        return load_deep_lm_config(path, train_input_path, test_input_path)
    elif model_name == "deepcls/textcnn":
        return load_deep_cls_cnn_config(path, train_input_path, test_input_path)
    elif model_name == "deepcls/textrnn":
        return load_deep_cls_rnn_config(path, train_input_path, test_input_path)
    elif model_name == "deepemb/skip-thought":
        return load_deep_emb_skip_thought_config(path, train_input_path, test_input_path)
    elif model_name == "deepmatch/cdssm":
        return load_deep_match_cdssm_config(path, train_input_path, test_input_path)
    elif model_name == "deepocr/cnn-lstm-ctc":
        return load_deep_ocr_config(path, train_input_path, test_input_path)


def load_deep_crf_config(path, train_input_path=None, test_input_path=None):
    with open(path, "r") as fp:
        json_str = fp.read()
        return DeepCRFConfig(json_str, train_input_path, test_input_path)


def load_deep_lm_config(path, train_input_path=None, test_input_path=None):
    with open(path, "r") as fp:
        json_str = fp.read()
        return DeepLMConfig(json_str, train_input_path, test_input_path)


def load_deep_cls_cnn_config(path, train_input_path=None, test_input_path=None):
    with open(path, "r") as fp:
        json_str = fp.read()
        return TextCNNConfig(json_str, train_input_path, test_input_path)


def load_deep_cls_rnn_config(path, train_input_path=None, test_input_path=None):
    with open(path, "r") as fp:
        json_str = fp.read()
        return TextRNNConfig(json_str, train_input_path, test_input_path)


def load_deep_emb_skip_thought_config(path, train_input_path=None, test_input_path=None):
    with open(path, "r") as fp:
        json_str = fp.read()
        return SkipThoughtConfig(json_str, train_input_path, test_input_path)


def load_deep_match_cdssm_config(path, train_input_path=None, test_input_path=None):
    with open(path, "r") as fp:
        json_str = fp.read()
        return CDSSMConfig(json_str, train_input_path, test_input_path)


def load_deep_ocr_config(path, train_input_path=None, test_input_path=None):
    with open(path, "r") as fp:
        json_str = fp.read()
        return DeepOCRConfig(json_str, train_input_path, test_input_path)

