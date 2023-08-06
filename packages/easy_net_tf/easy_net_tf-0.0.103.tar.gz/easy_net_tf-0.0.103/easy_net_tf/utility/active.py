import tensorflow as tf


class UtilityActive:
    @staticmethod
    def prelu(features, name):
        alphas = tf.get_variable('%s/prelu_alpha' % name, features.get_shape()[-1],
                                 initializer=tf.constant_initializer(0.0),
                                 dtype=tf.float32)
        pos = tf.nn.relu(features)
        neg = alphas * (features - abs(features)) * 0.5

        return pos + neg
