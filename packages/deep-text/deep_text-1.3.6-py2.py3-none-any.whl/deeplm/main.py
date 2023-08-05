from common import utils
from common import config_ops
from .model import GraphDeepLMModel
from .train import DeepLMTrainer
from .default_custom import DefaultTransform
import tensorflow as tf
import sys
import getopt


def main_learn():
    train_input_path = ""
    test_input_path = ""
    config_file_path = ""
    model_save_path = ""
    need_transform = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:e:c:m:fw",
                                   ["train=", "test=", "config=", "model="])
    except getopt.getopt.GetoptError:
        print('deeplm_learn -t <trainfile> -e <testfile> -c <configfile> -m <model save path> '
              '[-f <do transform>]')
        sys.exit(2)

    if len(opts) == 0:
        print('deeplm_learn -t <trainfile> -e <testfile> -c <configfile> -m <model save path> '
              '[-f <do transform>]')
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print('deeplm_learn -t <trainfile> -e <testfile> -c <configfile> -m <model save path> '
                  '[-f <do transform>]')
            sys.exit()
        elif opt in ("-t", "--train"):
            train_input_path = arg
        elif opt in ("-e", "--test"):
            test_input_path = arg
        elif opt in ("-c", "--config"):
            config_file_path = arg
        elif opt in ("-m", "--model"):
            model_save_path = arg
        elif opt == "-f":
            need_transform = True

    if train_input_path == "":
        print("Please input -t or --train to set train_input_path.")
        sys.exit()

    if test_input_path == "":
        print("Please input -e or --test to set test_input_path.")
        sys.exit()

    if config_file_path == "":
        print("Please input -c or --config to set config_file_path.")
        sys.exit()

    if model_save_path == "":
        print("Please input -m or --model to set model_save_path.")
        sys.exit()

    config = config_ops.load_deep_lm_config(config_file_path, train_input_path, test_input_path)

    trainer = DeepLMTrainer(config, DefaultTransform, need_transform)

    model = trainer.train()
    model.save(model_save_path)


def main_eval():
    test_input_path = ""
    output_path = ""
    config_file_path = ""
    model_path = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:],"he:o:c:m:",["test=","output=", "config=","model="])
    except getopt.getopt.GetoptError:
        print('deeplm_eval -e <test file> -c <config file> -m <model save path>')
        sys.exit(2)
        
    if len(opts) == 0:
        print('deeplm_eval -e <test file> -c <config file> -m <model file path>')
        sys.exit()
        
    for opt, arg in opts:
        if opt == '-h':
            print('deeplm_eval -e <test file> -c <config file> -m <model file path>')
            sys.exit()
        elif opt in ("-e", "--test"):
            test_input_path = arg
        elif opt in ("-o", "--output"):
            output_path = arg
        elif opt in ("-c", "--config"):
            config_file_path = arg
        elif opt in ("-m", "--model"):
            model_path = arg
        
    if test_input_path == "":
        print("Please input -e or --test to set test_input_path.")
        sys.exit()
         
    if output_path == "":
        print("Default output filename: eval-out.txt")
        output_path = "eval-out.txt"
        
    if config_file_path == "":
        print("Please input -c or --config to set config_file_path.")
        sys.exit()
            
    if model_path == "":
        print("Please input -m or --model to set model_path.")
        sys.exit()
     
    config = config_ops.load_deep_lm_config(config_file_path)
    model = GraphDeepLMModel(model_path, config, DefaultTransform)
    
    ofp = open(output_path, "w")
    with open(test_input_path, "r") as fp:
        rets = model.eval(fp)
        for ret in rets:
            for pred in ret:
                ptags = "\n".join([p[0] + "\t" + p[1] for p in pred])
                ofp.write(ptags + "\n\n")
    ofp.flush()
    ofp.close()


def main_save():
    checkpoint_path = ""
    model_save_path = ""
    config_file_path = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:p:m:", ["checkpoint=", "model="])
    except getopt.getopt.GetoptError:
        print('deeplm_save -p <checkpoint path> -c <config path> -m <model file path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('deeplm_save -p <checkpoint path> -c <config path> -m <model file path>')
            sys.exit()
        elif opt in ("-p", "--checkpoint"):
            checkpoint_path = arg
        elif opt in ("-m", "--model"):
            model_save_path = arg
        elif opt in ("-c", "--config"):
            config_file_path = arg

    if checkpoint_path == "":
        print("Please input -p or --checkpoint to set checkpoint_path.")
        sys.exit()

    if model_save_path == "":
        print("Please input -m or --model to set model_save_path.")
        sys.exit()

    if config_file_path == "":
        print("Please input -c or --config to set config_file_path.")
        sys.exit()

    config = config_ops.load_deep_lm_config(config_file_path)

    checkpoint_file = tf.train.latest_checkpoint(checkpoint_path)
    sess = utils.load_session(checkpoint_file, config)

    scope = ""
    if len(config.gpu_list) > 0:
        scope = "reuse_model/"
    scopes = [scope+"logits/probs",
              scope+"logits/logits",
              scope+"scores/sequence_scores"]
    graph = tf.graph_util.convert_variables_to_constants(sess, sess.graph_def, scopes)
    with tf.gfile.GFile(model_save_path+".pb", "wb") as f:
        f.write(graph.SerializeToString())

