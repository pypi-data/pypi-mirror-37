import tensorflow as tf
import numpy as np
import sys

__all__ = ['cal_num_parameters', 'delete_and_make_dir', 'read_events_file', 'create_op_graph', 'count_model_params',
           'Logger']


def cal_num_parameters():
    return np.sum(list(map(lambda tv: np.prod(tv.get_shape().as_list()), tf.trainable_variables())))


def delete_and_make_dir(dir):
    if tf.gfile.Exists(dir):
        tf.gfile.DeleteRecursively(dir)
    tf.gfile.MakeDirs(dir)


def read_events_file(events_filename):
    events_iter = tf.train.summary_iterator(events_filename)
    _ = next(events_iter)
    dt = {'step': []}
    for elem in events_iter:
        dt['step'].append(elem.step)
        for e in elem.summary.value:
            if e.tag in dt:
                dt[e.tag].append(e.simple_value)
            else:
                dt[e.tag] = [e.simple_value]
    return dt


def create_op_graph(graph_def):
    g = tf.Graph()
    with g.as_default():
        tf.import_graph_def(graph_def, name='')
    return g


def count_model_params(tf_variables):
    num_vars = 0
    for var in tf_variables:
        num_vars += np.prod([dim.value for dim in var.get_shape()])
    return num_vars


class Logger:
    def __init__(self, output_file):
        self.terminal = sys.stdout
        self.log = open(output_file, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        pass
