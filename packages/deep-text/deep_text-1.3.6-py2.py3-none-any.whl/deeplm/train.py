# -*- coding=utf-8 -*-

from common import utils
from common.train import Trainer
from .model import Bi_GRU_LM
import logging


class DeepLMTrainer(Trainer):
    def __init__(self, config, _transform_class, need_transform=False,
                 restore_model=False, optimizer=None):
        super(DeepLMTrainer, self).__init__(config, _transform_class, Bi_GRU_LM,
                                            need_transform, False, restore_model, optimizer)

    def train_step(self, batch_data):
        feed_dict = {
            self.model.input: batch_data["doc_batch"],
            self.model.labels: batch_data["label_batch"],
            self.model.sequence_lengths: batch_data["seq_lens"],
            self.model.weights: batch_data["weights"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob,
        }

        _, step, summaries, loss = self.session.run(self.train_ops, feed_dict)

        logging.info("step {}, loss {:g}".format(step, loss))
        self.train_summary_writer.add_summary(summaries, step)

    def dev_step(self, batch_data):
        feed_dict = {
            self.model.input: batch_data["doc_batch"],
            self.model.labels: batch_data["label_batch"],
            self.model.sequence_lengths: batch_data["seq_lens"],
            self.model.weights: batch_data["weights"],
            self.model.input_keep_prob: 1.,
            self.model.output_keep_prob: 1.,
        }

        step, summaries, loss = self.session.run(self.dev_ops, feed_dict)

        logging.info("step {}, loss {:g}".format(step, loss))
        self.dev_summary_writer.add_summary(summaries, step)
