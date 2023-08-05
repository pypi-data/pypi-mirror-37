import tensorflow as tf
from common import utils
import numpy as np
from PIL import Image
from common.model import BaseModel
from .default_custom import DeepOCRTransform


class DeepOCRModel(BaseModel):
    def __init__(self, session, transformer, config):
        super(DeepOCRModel, self).__init__(session, transformer, config)
        self.input = None
        self.labels = None
        self.sequence_lengths = None
        self.label_lengths = None
        self.input_keep_prob = None
        self.output_keep_prob = None
        self.dense_decoded = None

    def predict(self, images):
        image_arr = []
        for image in images:
            image = image.resize(self.config.image_shape, Image.ANTIALIAS)
            image = np.array(image).reshape((self.config.image_shape[0], self.config.image_shape[1], -1))
            image_arr.append(np.array(image))
        time_steps = [self.config.sequence_length] * len(images)
        feed_dict = {self.input: image_arr,
                     self.sequence_lengths: np.array(time_steps),
                     self.input_keep_prob: 1.0,
                     self.output_keep_prob: 1.0}

        decode = self.session.run([self.dense_decoded], feed_dict=feed_dict)[0]
        return self.transformer.transform_labels(decode)


class GraphDeepOCRModel(DeepOCRModel):
    def __init__(self, model_path, config, TransformClass=None):
        if TransformClass is None:
            super(GraphDeepOCRModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), DeepOCRTransform(config), config)
        else:
            super(GraphDeepOCRModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), TransformClass(config), config)
        self.transformer.load_pre_data()
        self.session.as_default()
        self.input = self.session.graph.get_tensor_by_name("input:0")
        self.sequence_lengths = self.session.graph.get_tensor_by_name("sequence_lengths:0")
        self.input_keep_prob = self.session.graph.get_tensor_by_name("input_keep_prob:0")
        self.output_keep_prob = self.session.graph.get_tensor_by_name("output_keep_prob:0")
        self.dense_decoded = self.session.graph.get_tensor_by_name("decoded/dense_decoded:0")

