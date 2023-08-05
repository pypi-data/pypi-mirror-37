# -*- coding=utf-8 -*-
from abc import abstractmethod

from . import utils
import tensorflow as tf
import os
import shutil
import logging


class MultiGPUTrainer(object):
    def __init__(self, config, _transform_class, _model_class, need_transform=False, rebuild_word2vec=False,
                 restore_model=False, optimizer=None, summaries=None):
        if summaries is None:
            summaries = ["loss", "accuracy", "auc"]
        self.restore_model = restore_model
        self.train_ops = []
        self.dev_ops = []
        self.config = config
        self.graph = tf.Graph()
        with self.graph.as_default():
            session_conf = tf.ConfigProto(
              allow_soft_placement=config.allow_soft_placement,
              log_device_placement=config.log_device_placement)
            session_conf.gpu_options.allow_growth = True
            self.session = tf.Session(config=session_conf, graph=self.graph)
            with self.session.as_default():
                self.transformer = _transform_class(config)
                if need_transform:
                    self.transformer.transform(rebuild_word2vec)
                else:
                    self.transformer.load()

                with tf.device('/cpu:0'):
                    with tf.variable_scope("reuse_model", reuse=False):
                        self.eval_model = _model_class(self.session, self.transformer, self.config)

                self.global_step = tf.Variable(0, name="global_step", trainable=False)

                self.optimizer = optimizer
                if self.optimizer is None:
                    self.optimizer = tf.train.AdamOptimizer(config.lr)

                self.models = []
                tower_grads = []
                with tf.name_scope("train") as train_scope:
                    for i in config.gpu_list:
                        with tf.device('/gpu:%d' % i):
                            with tf.name_scope('GPU_%d' % i):
                                with tf.variable_scope("reuse_model", reuse=True):
                                    train_model = _model_class(self.session, self.transformer, self.config)
                                    self.models.append(train_model)
                                    for summary in summaries:
                                        if hasattr(train_model, summary):
                                            tf.add_to_collection(summary, getattr(train_model, summary))

                                    grads = self.optimizer.compute_gradients(train_model.loss)
                                    grads_clip = [[tf.clip_by_value(g,
                                                                    -self.config.gradient_clip,
                                                                    self.config.gradient_clip),
                                                   v] for g, v in grads]
                                    tower_grads.append(grads_clip)

                grads = self.average_gradients(tower_grads)
                train_op = self.optimizer.apply_gradients(grads, global_step=self.global_step)

                self.train_ops.append(train_op)
                self.train_ops.append(self.global_step)
                self.dev_ops.append(self.global_step)

                self.saver = tf.train.Saver(max_to_keep=config.num_checkpoints)

                # Summaries
                summary_scalars_train = []
                summary_scalars_dev = []
                for summary in summaries:
                    if hasattr(self.eval_model, summary):
                        summary_mean = tf.reduce_mean(tf.get_collection(summary, train_scope))
                        summary_scalar = tf.summary.scalar(summary, summary_mean)
                        summary_scalars_train.append(summary_scalar)
                        summary_scalar = tf.summary.scalar(summary, getattr(self.eval_model, summary))
                        summary_scalars_dev.append(summary_scalar)

                train_summary_op = tf.summary.merge(summary_scalars_train)
                dev_summary_op = tf.summary.merge(summary_scalars_dev)
                self.train_ops.append(train_summary_op)
                self.dev_ops.append(dev_summary_op)

                for summary in summaries:
                    if hasattr(self.eval_model, summary):
                        summary_mean = tf.reduce_mean(tf.get_collection(summary, train_scope))
                        self.train_ops.append(summary_mean)
                        self.dev_ops.append(getattr(self.eval_model, summary))

                # Output directory for models and summaries
                out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs"))
                checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
                ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
                if restore_model:
                    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
                    self.session.run(init_op)
                    self.saver.restore(self.session, ckpt.model_checkpoint_path)
                else:
                    if os.path.exists(out_dir + "/checkpoints"):
                        shutil.rmtree(out_dir + "/checkpoints")
                    if os.path.exists(out_dir + "/summaries"):
                        shutil.rmtree(out_dir + "/summaries")

                #Train Summaries
                train_summary_dir = os.path.join(out_dir, "summaries", "train")
                self.train_summary_writer = tf.summary.FileWriter(train_summary_dir, self.graph)

                # Dev summaries
                dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
                self.dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, self.graph)

                # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
                self.checkpoint_prefix = os.path.join(checkpoint_dir, "model")
                if not os.path.exists(checkpoint_dir):
                    os.makedirs(checkpoint_dir)

                self.checkpoint_index_dev = os.path.join(out_dir, "summaries", "dev", "checkpoint")
                self.checkpoint_index = os.path.join(checkpoint_dir, "checkpoint")

                if not self.restore_model:
                    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
                    self.session.run(init_op)

    def train(self):
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord, sess=self.session)
        try:
            while not coord.should_stop():
                datas = []
                for i in range(len(self.models)):
                    data = self.transformer.pull_batch(self.session)
                    datas.append(data)
                self.train_step(datas)
                current_step = tf.train.global_step(self.session, self.global_step)
                if current_step % self.config.evaluate_every == 0:
                    logging.info("\nEvaluation:")
                    self.dev_step(self.transformer.get_test_data())
                    logging.info("")
                if current_step % self.config.checkpoint_every == 0:
                    path = self.saver.save(self.session, self.checkpoint_prefix, global_step=current_step)
                    utils.copy_file(self.checkpoint_index, self.checkpoint_index_dev)
                    logging.info("Saved model checkpoint to {}\n".format(path))
        except tf.errors.OutOfRangeError:
            logging.info ('Done training -- epoch limit reached')

        coord.request_stop()
        coord.join(threads)
        return self.eval_model

    def average_gradients(self, tower_grads):
        average_grads = []
        for grad_and_vars in zip(*tower_grads):
            grads = []
            for g, _ in grad_and_vars:
                expanded_g = tf.expand_dims(g, 0)
                grads.append(expanded_g)
            grad = tf.concat(grads, 0)
            grad = tf.reduce_mean(grad, 0)

            v = grad_and_vars[0][1]
            grad_and_var = (grad, v)
            average_grads.append(grad_and_var)
        return average_grads

    @abstractmethod
    def train_step(self, batch_datas):
        pass

    @abstractmethod
    def dev_step(self, batch_data):
        pass

