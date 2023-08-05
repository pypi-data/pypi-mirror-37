from deepcrf.config import DeepCRFConfig
from deeplm.config import DeepLMConfig
from deepcls.config import TextCNNConfig
from deepcls.config import TextRNNConfig
from deepmatch.config import CDSSMConfig
from deepemb.config import SkipThoughtConfig
from deepocr.config import DeepOCRConfig
import sys
import getopt


def generate_config_file():
    model = ""
    path = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:o:", ["model=", "output="])
    except getopt.getopt.GetoptError:
        print('deeptext_gen_config -m <deepcrf|cls-rnn|cls-cnn> -o <output path>')
        sys.exit(2)

    if len(opts) == 0:
        print('deeptext_gen_config -m <deepcrf|cls-rnn|cls-cnn> -o <output path>')
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print('deeptext_gen_config -m <deepcrf|cls-rnn|cls-cnn> -o <output path>')
            sys.exit()
        elif opt in ("-o", "--output"):
            path = arg
        elif opt in ("-m", "--model"):
            model = arg

    if model == "deepcrf" or model == "deep-crf":
        config = DeepCRFConfig("{}", "", "")
        config.dump(path)
        config.show()
    elif model == "textcnn" or model == "clscnn":
        config = TextCNNConfig("{}", "", "")
        config.dump(path)
        config.show()
    elif model == "textrnn" or model == "clsrnn":
        config = TextRNNConfig("{}", "", "")
        config.dump(path)
        config.show()
    elif model == "lm" or model == "deeplm":
        config = DeepLMConfig("{}", "", "")
        config.dump(path)
        config.show()
    elif model == "cdssm" or model == "cdssm":
        config = CDSSMConfig("{}", "", "")
        config.dump(path)
        config.show()
    elif model == "skip-thought" or model == "stemb":
        config = SkipThoughtConfig("{}", "", "")
        config.dump(path)
        config.show()
    elif model == "deepocr" or model == "lstm-ctc":
        config = DeepOCRConfig("{}", "", "")
        config.dump(path)
        config.show()

