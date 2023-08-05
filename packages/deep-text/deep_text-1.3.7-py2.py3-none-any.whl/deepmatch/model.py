from abc import abstractmethod

import tensorflow as tf
from common import utils
from common.model import BaseModel
from deepmatch.default_custom import DefaultTransform


class DeepMatchModel(BaseModel):
    def __init__(self, session, transformer, config):
        super(DeepMatchModel, self).__init__(session, transformer, config)
        self.input_doc1 = None
        self.input_doc2 = None
        self.labels = None
        self.batch_size = None
        self.dropout_keep_prob = None
        self.doc1_vector = None
        self.doc2_vector = None
        self.similarity = None

    @abstractmethod
    def predict(self, docs, top_n):
        pass


class GraphCDSSMModel(DeepMatchModel):
    def __init__(self, model_path, config, TransformClass=None):
        if TransformClass is None:
            super(GraphCDSSMModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), DefaultTransform(config), config)
        else:
            super(GraphCDSSMModel, self).__init__(tf.Session(graph=utils.load_graph_file(model_path)), TransformClass(config), config)
        self.transformer.load_pre_data()
        self.session.as_default()
        self.input_doc1 = self.session.graph.get_tensor_by_name("input_doc1:0")
        self.input_doc2 = self.session.graph.get_tensor_by_name("input_doc2:0")
        self.batch_size = self.session.graph.get_tensor_by_name("batch_size:0")
        self.input_keep_prob = self.session.graph.get_tensor_by_name("input_keep_prob:0")
        self.output_keep_prob = self.session.graph.get_tensor_by_name("output_keep_prob:0")
        self.doc1_vector = self.session.graph.get_tensor_by_name("cnn_doc1/doc_vector:0")
        self.doc2_vector = self.session.graph.get_tensor_by_name("cnn_doc2/doc_vector:0")
        self.similarity = self.session.graph.get_tensor_by_name("output/similarity:0")

    def predict(self, doc1s, doc2s):
        doc1_ids = self.transformer.transform_docs(doc1s, True)
        doc2_ids = self.transformer.transform_docs(doc2s, False)
        feed_dict = {self.input_doc1: doc1_ids,
                     self.input_doc2: doc2_ids,
                     self.input_keep_prob: 1.0,
                     self.output_keep_prob: 1.0,
                     self.batch_size: len(doc1s)}

        return self.session.run([self.similarity], feed_dict=feed_dict)[0]

    def vectors_front(self, docs):
        doc_ids = self.transformer.transform_docs(docs)
        feed_dict = {self.input_doc1: doc_ids,
                     self.input_keep_prob: 1.0,
                     self.output_keep_prob: 1.0,
                     self.batch_size: len(docs)}

        return self.session.run([self.doc1_vector], feed_dict=feed_dict)[0]

    def vectors_back(self, docs):
        doc_ids = self.transformer.transform_docs(docs)
        feed_dict = {self.input_doc2: doc_ids,
                     self.input_keep_prob: 1.0,
                     self.output_keep_prob: 1.0,
                     self.batch_size: len(docs)}

        return self.session.run([self.doc2_vector], feed_dict=feed_dict)[0]


