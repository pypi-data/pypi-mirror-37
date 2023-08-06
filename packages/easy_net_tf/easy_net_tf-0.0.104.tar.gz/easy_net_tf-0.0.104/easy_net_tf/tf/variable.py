import tensorflow as tf
import tensorflow.contrib as tf_contrib


class UtilityVariable:

    @staticmethod
    def initialize_weight(shape,
                          l2_regular=('l2_regular', 0.0005),
                          name=''):
        """

        :param shape:
        :param l2_regular: a tuple (name of l2_regular cancel if None, importance)
        :param name:
        :return:
        """
        kernel = tf.truncated_normal(shape, stddev=0.1)

        if l2_regular[0] is not None:
            tf.add_to_collection(
                name=l2_regular[0],
                value=tf_contrib.layers.l2_regularizer(scale=l2_regular[1])(kernel)
            )

        return tf.Variable(kernel, name=name)

    @staticmethod
    def initialize_bias(shape, name=''):
        initial = tf.constant(0.1, shape=shape)

        return tf.Variable(initial, name=name)
