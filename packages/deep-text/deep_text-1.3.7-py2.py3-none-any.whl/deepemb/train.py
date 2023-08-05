# -*- coding=utf-8 -*-

from common.train import Trainer
from common.train_mgpu import MultiGPUTrainer
from .skip_thought import SkipThought
import logging


class SkipThoughtTrainer(Trainer):
    def __init__(self, config, _transform_class, need_transform=False, rebuild_word2vec=False,
                 restore_model=False, optimizer=None):
        super(SkipThoughtTrainer, self).__init__(config, _transform_class, SkipThought,
                                                 need_transform, rebuild_word2vec,
                                                 restore_model, optimizer)

    def train_step(self, batch_data):
        feed_dict = {
            self.model.input: batch_data["inputs"],
            self.model.input_lengths: batch_data["input_lens"],
            self.model.output_prev_input: batch_data["output_prevs"],
            self.model.output_prev_target: batch_data["target_prevs"],
            self.model.output_prev_lengths: batch_data["prev_lens"],
            self.model.prev_weights: batch_data["prev_weights"],
            self.model.output_post_input: batch_data["output_posts"],
            self.model.output_post_target: batch_data["target_posts"],
            self.model.output_post_lengths: batch_data["output_post_lens"],
            self.model.post_weights: batch_data["post_weights"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob,
        }

        _, step, summaries, loss, = self.session.run(self.train_ops, feed_dict)

        logging.info("step {}, loss {:g}".format(step, loss))
        self.train_summary_writer.add_summary(summaries, step)

    def dev_step(self, batch_data):
        feed_dict = {
            self.model.input: batch_data["inputs"],
            self.model.input_lengths: batch_data["input_lens"],
            self.model.output_prev_input: batch_data["output_prevs"],
            self.model.output_prev_target: batch_data["target_prevs"],
            self.model.output_prev_lengths: batch_data["prev_lens"],
            self.model.prev_weights: batch_data["prev_weights"],
            self.model.output_post_input: batch_data["output_posts"],
            self.model.output_post_target: batch_data["target_posts"],
            self.model.output_post_lengths: batch_data["output_post_lens"],
            self.model.post_weights: batch_data["post_weights"],
            self.model.input_keep_prob: self.config.input_keep_prob,
            self.model.output_keep_prob: self.config.output_keep_prob,
        }

        step, summaries, loss = self.session.run(self.dev_ops, feed_dict)

        logging.info("step {}, loss {:g}".format(step, loss))
        self.dev_summary_writer.add_summary(summaries, step)


class SkipThoughtMultiGPUTrainer(MultiGPUTrainer):
    def __init__(self, config, _transform_class, need_transform=False, rebuild_word2vec=False,
                 restore_model=False, optimizer=None):
        super(SkipThoughtMultiGPUTrainer, self).__init__(config, _transform_class, SkipThought,
                                                         need_transform, rebuild_word2vec,
                                                         restore_model, optimizer)

    def train_step(self, batch_data):
        feed_dict = {}
        for i in range(len(self.models)):
            model = self.models[i]
            feed_dict[model.input] = batch_data[i]["inputs"]
            feed_dict[model.input_lengths] = batch_data[i]["input_lens"]
            feed_dict[model.output_prev_input] = batch_data[i]["output_prevs"]
            feed_dict[model.output_prev_target] = batch_data[i]["target_prevs"]
            feed_dict[model.output_prev_lengths] = batch_data[i]["prev_lens"]
            feed_dict[model.prev_weights] = batch_data[i]["prev_weights"]
            feed_dict[model.output_post_input] = batch_data[i]["output_posts"]
            feed_dict[model.output_post_target] = batch_data[i]["target_posts"]
            feed_dict[model.output_post_lengths] = batch_data[i]["output_post_lens"]
            feed_dict[model.post_weights] = batch_data[i]["post_weights"]
            feed_dict[model.input_keep_prob] = self.config.input_keep_prob
            feed_dict[model.output_keep_prob] = self.config.output_keep_prob

        _, step, summaries, loss, = self.session.run(self.train_ops, feed_dict)

        logging.info("step {}, loss {:g}".format(step, loss))
        self.train_summary_writer.add_summary(summaries, step)

    def dev_step(self, batch_data):
        feed_dict = {
            self.eval_model.input: batch_data["inputs"],
            self.eval_model.input_lengths: batch_data["input_lens"],
            self.eval_model.output_prev_input: batch_data["output_prevs"],
            self.eval_model.output_prev_target: batch_data["target_prevs"],
            self.eval_model.output_prev_lengths: batch_data["prev_lens"],
            self.eval_model.prev_weights: batch_data["prev_weights"],
            self.eval_model.output_post_input: batch_data["output_posts"],
            self.eval_model.output_post_target: batch_data["target_posts"],
            self.eval_model.output_post_lengths: batch_data["output_post_lens"],
            self.eval_model.post_weights: batch_data["post_weights"],
            self.eval_model.input_keep_prob: self.config.input_keep_prob,
            self.eval_model.output_keep_prob: self.config.output_keep_prob,
        }

        step, summaries, loss = self.session.run(self.dev_ops, feed_dict)

        logging.info("step {}, loss {:g}".format(step, loss))
        self.dev_summary_writer.add_summary(summaries, step)

