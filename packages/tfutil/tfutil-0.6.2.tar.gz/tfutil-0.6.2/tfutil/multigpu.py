import tensorflow as tf
import collections
from .misc import delete_and_make_dir
from .tftrain import load_ckpt, load_ckpt_path, create_init_op
from tqdm import trange, tnrange

__all__ = ['MultiGPUModelTensors', 'MGTFModel']

MultiGPUModelTensors = collections.namedtuple('MultiGPUModelTensors',
                                              ('inputs',
                                               'labels',
                                               'is_training',
                                               'model',
                                               'train_input_func',
                                               'loss_func',
                                               'optimizer'))


class MGTFModel:
    def __init__(self, model_tensors: MultiGPUModelTensors, n_gpu, ckpt_dir=None, is_notebook=False):
        self.inputs = model_tensors.inputs
        self.labels = model_tensors.labels
        self.is_training = model_tensors.is_training
        self.model = model_tensors.model
        self.train_input_func = model_tensors.train_input_func
        self.loss_func = model_tensors.loss_func
        self.optimizer = model_tensors.optimizer
        self.n_gpu = n_gpu
        self.ckpt_dir = ckpt_dir
        self.sess = None
        self.model_loaded = False
        self.is_notebook = is_notebook
        with tf.name_scope('main'):
            self.logits = self.model(self.inputs, self.is_training)

        if self.is_notebook:
            self.progress_range = tnrange
        else:
            self.progress_range = trange
        self._build_training_graph()

    def load_weights(self, sess, ckpt_path=None):
        self.sess = sess
        if ckpt_path is None:
            load_ckpt(sess, self.ckpt_dir)
        else:
            load_ckpt_path(sess, ckpt_path)
        self.model_loaded = True

    @classmethod
    def average_grad(cls, tower_grads):
        average_grads = []
        for grad_and_vars in zip(*tower_grads):
            grads = []
            for g, _ in grad_and_vars:
                expanded_g = tf.expand_dims(g, 0)
                grads.append(expanded_g)
            grad = tf.reduce_mean(tf.concat(grads, 0), axis=0)
            v = grad_and_vars[0][1]
            grad_and_var = (grad, v)
            average_grads.append(grad_and_var)
        return average_grads

    def _build_training_graph(self):
        with tf.device('/cpu:0'):
            global_step = tf.train.get_or_create_global_step()
            tower_grads = []
            losses = []
            for i in range(self.n_gpu):
                with tf.device(f'/gpu:{i}'):
                    with tf.name_scope(f'GPU_{i}'):
                        (x, y), _ = self.train_input_func()
                        logits = self.model(x, True)
                        loss = self.loss_func(y, logits)
                        grads = self.optimizer.compute_gradients(loss)
                        tower_grads.append(grads)
                        losses.append(loss)
            self.loss = tf.reduce_mean(losses)
            grads = self.average_grad(tower_grads)
            self.train_op = self.optimizer.apply_gradients(grads, global_step=global_step)

    def train(self, num_steps, ckpt_steps, metric_opdefs, extra_summ_ops=None, listeners=None,
              max_ckpt_to_keep=10, summ_steps=100, sess_config_proto=None,
              graph=None, from_scratch=True):
        metric_ops, update_ops, reset_ops, _, _ = list(zip(*metric_opdefs))
        metric_summ_names = ['train/{0}'.format(m.name.split('/')[-2]) for m in metric_ops]
        metric_summ_ops = [tf.summary.scalar(*tup) for tup in list(zip(metric_summ_names, metric_ops))]
        summ_ops = metric_summ_ops + list(extra_summ_ops) if extra_summ_ops else metric_summ_ops
        summ_op = tf.summary.merge(summ_ops)
        summ_loss_op = tf.summary.scalar('train/loss', self.loss)
        if from_scratch:
            delete_and_make_dir(self.ckpt_dir)
        global_step = tf.train.get_or_create_global_step()
        data_gntr, _ = self.train_input_func()
        num_ckpts = num_steps // ckpt_steps
        saver = tf.train.Saver(max_to_keep=max_ckpt_to_keep)
        summ_writer = tf.summary.FileWriter(f'{self.ckpt_dir}/train')

        if listeners:
            for l in listeners:
                l.begin(self.ckpt_dir, self.inputs, self.labels, self.is_training, self.logits, ckpt_steps)
        if graph is not None:
            # summ_writer.add_graph(tf.get_default_graph()) # debug
            summ_writer.add_graph(graph)
        if sess_config_proto is None:
            sess_config_proto = tf.ConfigProto(allow_soft_placement=True)
            sess_config_proto.gpu_options.allow_growth = True
        else:
            sess_config_proto = sess_config_proto
        with tf.Session(config=sess_config_proto) as sess:
            sess.run(create_init_op())
            if not from_scratch:
                load_ckpt(sess, model_dir=self.ckpt_dir)
            global_step_val = sess.run(global_step)
            id_ckpt = global_step_val // ckpt_steps
            for _ in range(num_ckpts):
                progress_desc = f'Checkpoint {id_ckpt+1}'
                for _ in self.progress_range(ckpt_steps, desc=progress_desc):
                    xb, yb = sess.run(data_gntr)
                    fd = {self.inputs: xb, self.labels: yb, self.is_training: True}
                    if global_step_val == 0:
                        sess.run(update_ops, feed_dict=fd)
                        summ = sess.run(summ_op, feed_dict=fd)
                        summ_writer.add_summary(summ, global_step=global_step_val)
                        sess.run(reset_ops)
                    summ_loss, _ = sess.run([summ_loss_op, self.train_op])
                    global_step_val = sess.run(global_step)
                    if global_step_val % summ_steps == 0:
                        sess.run(update_ops, feed_dict=fd)
                        summ = sess.run(summ_op, feed_dict=fd)
                        summ_writer.add_summary(summ, global_step=global_step_val)
                        summ_writer.add_summary(summ_loss, global_step=global_step_val)
                        sess.run(reset_ops)
                id_ckpt = global_step_val // ckpt_steps
                summ_writer.flush()
                saver.save(sess, f'{self.ckpt_dir}/model.ckpt', global_step_val, write_meta_graph=False)
                if listeners:
                    for l in listeners:
                        l.run(sess, global_step_val, self.is_notebook)
            if listeners:
                for l in listeners:
                    l.end()
