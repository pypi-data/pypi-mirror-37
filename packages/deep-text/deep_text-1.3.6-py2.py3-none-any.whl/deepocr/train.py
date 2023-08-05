# -*- coding=utf-8 -*-

from common import utils
from common.train import Trainer
from .cnn_lstm_ctc import CNN_LSTM_CTC
import numpy as np
import logging


class DeepOCRTrainer(Trainer):
    def __init__(self, config, _transform_class, need_transform=False, rebuild_word2vec=False,
                 restore_model=False, optimizer=None):
        super(DeepOCRTrainer, self).__init__(config, _transform_class, CNN_LSTM_CTC,
                                             need_transform, rebuild_word2vec,
                                             restore_model, optimizer)

    def train_step(self, batch_data):
        feed_dict = {
            self.model.input: batch_data["images"],
            self.model.labels: batch_data["labels"],
            self.model.sequence_lengths: batch_data["time_step"],
            self.model.label_lengths: batch_data["label_len"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob
        }

        _, step, summaries, loss = self.session.run(self.train_ops, feed_dict)
        logging.info("step {}, loss {:g}".format(step, loss))
        self.train_summary_writer.add_summary(summaries, step)

    def dev_step(self, batch_data):
        feed_dict = {
            self.model.input: batch_data["images"],
            self.model.labels: batch_data["labels"],
            self.model.sequence_lengths: batch_data["time_step"],
            self.model.label_lengths: batch_data["label_len"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob
        }

        step, summaries, loss = self.session.run(self.dev_ops, feed_dict)
        logging.info("step {}, loss {:g}".format(step, loss))
        self.dev_summary_writer.add_summary(summaries, step)

