import numpy as np
import tensorflow as tf
import collections
from .misc import delete_and_make_dir, create_op_graph
from .tftrain import load_ckpt, load_ckpt_path, create_init_op
from .visualization import saliency_grad
from tqdm import trange

__all__ = ['average_grad', 'ModelTensors', 'TFModel']


def average_grad(tower_grads):
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


ModelTensors = collections.namedtuple('ModelTensors',
                                      ('inputs',
                                       'labels',
                                       'is_training',
                                       'model',
                                       'train_input_func',
                                       'loss_func',
                                       'optimizer'))


class TFModel:
    def __init__(self, model_tensors: ModelTensors, n_gpu, ckpt_dir=None, training=True):
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
        with tf.name_scope('main'):
            self.logits = self.model(self.inputs, self.is_training)
        self.progress_range = trange
        if training:
            with tf.name_scope('training'):
                self._build_training_graph()

    def load_weights(self, sess, ckpt_path=None):
        self.sess = sess
        if ckpt_path is None:
            load_ckpt(sess, self.ckpt_dir)
        else:
            load_ckpt_path(sess, ckpt_path)
        self.model_loaded = True
        self.graph_def = sess.graph_def

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
            grads = average_grad(tower_grads)
            self.train_op = self.optimizer.apply_gradients(grads, global_step=global_step)
        self.graph_def = tf.get_default_graph().as_graph_def()

    def train(self,
              num_steps,
              summ_steps,
              ckpt_steps,
              metric_opdefs,
              extra_summ_ops=None,
              listeners=None,
              max_ckpt_to_keep=10,
              sess_config_proto=None,
              from_scratch=True):
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
        summ_writer.add_graph(create_op_graph(self.graph_def))
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
                        l.run(sess, global_step_val)
            if listeners:
                for l in listeners:
                    l.end()
            summ_writer.close()

    def predict(self, gnte_pred):
        data_gn, steps_per_epoch = gnte_pred
        logits_lst = []
        if not self.model_loaded:
            raise RuntimeError('Load model first!')
        sess = self.sess
        progress_desc = 'Test predict'
        for _ in self.progress_range(steps_per_epoch, desc=progress_desc):
            xb = sess.run(data_gn)
            fd = {self.inputs: xb, self.is_training: False}
            logits_val = sess.run(self.logits, feed_dict=fd)
            logits_lst.append(logits_val)
        logits = np.concatenate(logits_lst, axis=0)
        return logits

    def eval(self, metric_opdefs, gnte):
        data_gn, steps_per_epoch = gnte
        metric_ops, update_ops, reset_ops, _, _ = list(zip(*metric_opdefs))
        logits_lst = []
        if not self.model_loaded:
            raise RuntimeError('Load model first!')
        sess = self.sess
        sess.run(reset_ops)
        progress_desc = 'Test evaluation'
        for _ in self.progress_range(steps_per_epoch, desc=progress_desc):
            xb, yb = sess.run(data_gn)
            fd = {self.inputs: xb, self.labels: yb, self.is_training: False}
            logits_val, _ = sess.run([self.logits, update_ops], feed_dict=fd)
            logits_lst.append(logits_val)
        logits = np.concatenate(logits_lst, axis=0)
        metrics = sess.run(metric_ops)
        return logits, metrics

    def saliency_map_single(self, saliency_class, seed_x=None, niter=100, step=0.1):
        if seed_x is None:
            seed_x = np.zeros(shape=[1, *self.inputs.get_shape().as_list()[1:]], dtype=np.float32)
        sa_grads = saliency_grad(self.inputs, self.logits, saliency_class)
        x = np.copy(seed_x)
        probs = tf.nn.softmax(self.logits)
        sess = self.sess
        for i in range(niter):
            grads_val = sess.run(sa_grads, feed_dict={self.inputs: x, self.is_training: False})
            x += step * grads_val
            logits_value, probs_value = sess.run([self.logits, probs],
                                                 feed_dict={self.inputs: x, self.is_training: False})
            print(f'Iter: {i+1}')
            print(logits_value)
            print(probs_value)
        return x[0]

    def saliency_map_all(self, seed_x=None, niter=100, step=0.1):
        num_classes = self.logits.get_shape().as_list()[-1]
        if seed_x is None:
            seed_x = np.zeros(shape=[num_classes, *self.inputs.get_shape().as_list()[1:]], dtype=np.float32)
        probs = tf.nn.softmax(self.logits)
        sess = self.sess
        for c in range(num_classes):
            sa_grads = saliency_grad(self.inputs, self.logits, c)
            x = np.copy(seed_x[c])[None]
            for i in range(niter):
                grads_val = sess.run(sa_grads, feed_dict={self.inputs: x, self.is_training: False})
                x += step * grads_val
                logits_value, probs_value = sess.run([self.logits, probs],
                                                     feed_dict={self.inputs: x, self.is_training: False})
                print(f'Iter: {i+1}')
                print(logits_value)
                print(probs_value)
            seed_x[c] = x[0]
        logits_value, probs_value = sess.run([self.logits, probs],
                                             feed_dict={self.inputs: seed_x, self.is_training: False})
        print('Final result:')
        print(logits_value)
        print(probs_value)
        return seed_x
