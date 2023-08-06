import numpy
import tensorflow as tf
from easy_net_tf.utility.variable import UtilityVariable


class FCN:
    def __init__(self,
                 batch_input,
                 nodes_out,
                 add_bias=True,
                 normalize=False,
                 l2_regular=('l2_regular', 0.0005),
                 name=''):

        """

        :param batch_input: a Tensor [?, nodes_in]
        :param nodes_out: output nodes number
        :param add_bias:
        :param normalize:
        :param name: layer name
        """

        if batch_input is None:
            assert 'Error: [%s.%s] batch_image can not be ''None''.' % (FCN.__name__,
                                                                        FCN.__init__.__name__)
        else:
            _, _nodes_in = batch_input.shape
            self._nodes_in = _nodes_in.value
            assert self._nodes_in is not None, '[%s,%s] ' \
                                               'the dimension of input must be explicit, ' \
                                               'otherwise filters can not be initialized.' % (FCN.__name__,
                                                                                              FCN.__init__.__name__)

        self._nodes_out = nodes_out
        self._l2_regular = l2_regular
        self._name = name

        """
        initialize variable
        """
        self._weight, \
        self._bias = self._initialize_variable(
            add_bias=add_bias,
            name=name
        )

        """
        normalize variable
        """
        if normalize:
            self._weight = tf.nn.l2_normalize(self._weight,
                                              0,
                                              name='fcn_weight')

        """
        calculate
        """
        self._features = self._calculate(batch_input=batch_input)

    def _initialize_variable(self, add_bias, name=''):
        """

        :param name:
        :return:
        """
        weight = UtilityVariable.initialize_weight(
            shape=[self._nodes_in,
                   self._nodes_out],
            l2_regular=self._l2_regular,
            name='%s_fcn/weight' % name
        )

        bias = UtilityVariable.initialize_bias(
            [self._nodes_out],
            name='%s_fcn/bias' % name
        ) if add_bias else None

        return weight, bias

    def _calculate(self,
                   batch_input):
        """

        :param batch_input:
        :return: features
        """

        if self._bias is None:
            batch_output = tf.matmul(batch_input, self._weight)
        else:
            batch_output = tf.matmul(batch_input, self._weight) + self._bias

        return batch_output

    def get_features(self):
        """

        :return: features
        """
        return self._features

    def get_variables(self, sess=None, save_dir=None):
        """

        :return: weight, bias
        """

        if sess is None:
            return self._weight, self._bias
        else:
            weight = None if self._weight is None else sess.run(self._weight)
            bias = None if self._bias is None else sess.run(self._bias)

            if save_dir is not None:
                if weight is not None:
                    shape = '[%d,%d]' % weight.shape
                    numpy.savetxt(fname='%s/fcn-weight-%s.txt' % (save_dir, shape),
                                  X=weight,
                                  header='%s: weight' % FCN.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/fcn-weight-%s.npy' % (save_dir, shape),
                               arr=weight)

                if bias is not None:
                    shape = '[%d]' % bias.shape
                    numpy.savetxt(fname='%s/fcn-bias-%s.txt' % (save_dir, shape),
                                  X=bias,
                                  header='%s: bias' % FCN.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/fcn-bias-%s.npy' % (save_dir, shape),
                               arr=bias)

            return weight, bias

    def get_config(self):
        """
        export config as a list
        :return:
        """

        weight_shape = None if self._weight is None else self._weight.shape
        bias_shape = None if self._bias is None else self._bias.shape

        config = [
            '\n### %s\n' % self._name,
            '- Fully Connect Net\n',
            '- nodes in: %d\n' % self._nodes_in,
            '- nodes out: %d\n' % self._nodes_out,
            '- variables:\n',
            '   - weight: %s\n' % weight_shape,
            '   - bias: %s\n' % bias_shape,
            '- multiplicative amount: %d\n' % (self._nodes_in * self._nodes_out)
        ]
        return config


if __name__ == '__main__':
    from easy_net_tf.utility.file import UtilityFile
    from pathlib import Path

    image = numpy.array([[[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]]],
                        dtype=numpy.float32)

    image_ph = tf.placeholder(dtype=tf.float32, shape=[None, 60])

    fcn = FCN(batch_input=image_ph,
              nodes_out=30,
              add_bias=False,
              normalize=False,
              name='test')

    UtilityFile.save_str_list('test-fcn.md', fcn.get_config())
