# -*- coding=utf-8 -*-

from common.train import Trainer
from .cdssm import CDSSM
import logging


class CDSSMTrainer(Trainer):
    def __init__(self, config, _transform_class, need_transform=False, rebuild_word2vec=False,
                 restore_model=False, optimizer=None):
        super(CDSSMTrainer, self).__init__(config, _transform_class, CDSSM,
                                           need_transform, rebuild_word2vec,
                                           restore_model, optimizer)

    def train_step(self, batch_data):
        feed_dict = {
            self.model.input_doc1: batch_data["doc1_batch"],
            self.model.input_doc2: batch_data["doc2_batch"],
            self.model.labels: batch_data["label_batch"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob,
            self.model.batch_size: len(batch_data["label_batch"])
        }

        _, step, summaries, loss, auc = self.session.run(self.train_ops, feed_dict)

        logging.info("step {}, loss {:g}, auc {:g}".format(step, loss, auc))
        self.train_summary_writer.add_summary(summaries, step)

    def dev_step(self, batch_data):
        feed_dict = {
            self.model.input_doc1: batch_data["doc1_batch"],
            self.model.input_doc2: batch_data["doc2_batch"],
            self.model.labels: batch_data["label_batch"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob,
            self.model.batch_size: len(batch_data["label_batch"])
        }

        step, summaries, loss, auc = self.session.run(self.dev_ops, feed_dict)

        logging.info("step {}, loss {:g}, auc {:g}".format(step, loss, auc))
        self.dev_summary_writer.add_summary(summaries, step)

