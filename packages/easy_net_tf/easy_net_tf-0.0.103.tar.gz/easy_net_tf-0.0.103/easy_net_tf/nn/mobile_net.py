import numpy
import tensorflow as tf

from easy_net_tf.utility.variable import UtilityVariable


class MobileNet:
    VALID = 'VALID'
    SAME = 'SAME'

    def __init__(self,
                 batch_input,
                 dilate_number,
                 filter_size,
                 channels_out,
                 stride,
                 add_bias,
                 add_residual=False,
                 padding=SAME,
                 dilate_active_func=tf.nn.leaky_relu,
                 depth_active_func=tf.nn.leaky_relu,
                 l2_regular=('l2_regular', 0.0005),
                 name=''):
        """
        :param batch_input: a Tensor [batch, height, width, channel]
        :param dilate_number: if 'None', become MobileNet V1 without output activation
        :param filter_size:
        :param channels_out:
        :param stride:
        :param add_bias: True: add; False: not add
        :param add_residual: be sure input [height, width] = output [height, width]. stride=1 and padding='SAME'
        :param padding:
        :param dilate_active_func: active function for dilatation.
        :param depth_active_func: active function for depth-wise.
        :param name: layer name
        """

        """
        prepare
        """
        if batch_input is None:
            assert 'Error: [%s.%s] batch_image can not be ''None''.' % (MobileNet.__name__,
                                                                        MobileNet.__init__.__name__)
        else:
            _, _height_in, _width_in, _channels_in = batch_input.shape

            self._height_in = _height_in.value
            self._width_in = _width_in.value
            self._channels_in = _channels_in.value
            assert self._channels_in is not None, '[%s,%s] ' \
                                                  'the channels of input must be explicit, ' \
                                                  'otherwise filters can not be initialized.' % (MobileNet.__name__,
                                                                                                 MobileNet.__init__.__name__)

        self._channels_out = channels_out

        self._dilate_number = dilate_number

        self._filter_size = filter_size

        self._dilate_active_func = dilate_active_func
        self._dilate_active_func_name = 'None' \
            if self._dilate_active_func is None \
            else self._dilate_active_func.__name__

        self._depth_active_func = depth_active_func
        self._depth_active_func_name = 'None' \
            if self._depth_active_func is None \
            else self._depth_active_func.__name__

        self._l2_regular = l2_regular
        self._stride = stride

        if add_residual \
                and (stride != 1
                     or padding is not MobileNet.SAME):
            add_residual = False
            print('Error: '
                  '[%s.%s] '
                  'if residual added, '
                  'be sure stride = 1 and padding = %s.%s'
                  % (MobileNet.__name__,
                     MobileNet.__init__.__name__,
                     MobileNet.__name__,
                     MobileNet.SAME))
        self.add_residual = add_residual

        self.add_bias = add_bias
        self.padding = padding
        self.name = name

        """
        initialize filter
        """
        self.dilate_filter, \
        self.depth_filter, \
        self.compress_filter, \
        self.residual_filter, \
        self.bias = self._initialize_variable()

        """
        calculation
        """
        self.features = self._calculate(batch_input)

    def _initialize_variable(self):
        """
        initialize variable
        :return:
        """
        channel_multiplier = 1

        """
        dilatation_filter
        """
        channels_middle = self._channels_in \
            if self._dilate_number is None \
            else self._dilate_number

        dilatation_filter = None \
            if self._dilate_number is None \
            else UtilityVariable.initialize_weight(
            [1,
             1,
             self._channels_in,
             channels_middle],
            l2_regular=self._l2_regular,
            name='%s_mn/dilate' % self.name
        )

        """
        depth-wise_filter
        """
        depthwise_filter = UtilityVariable.initialize_weight(
            [self._filter_size,
             self._filter_size,
             channels_middle,
             channel_multiplier],
            l2_regular=self._l2_regular,
            name='%s_mn/depth' % self.name
        )

        """
        compress_filter
        """
        compress_filter = UtilityVariable.initialize_weight(
            [1,
             1,
             channels_middle * channel_multiplier,
             self._channels_out],
            l2_regular=self._l2_regular,
            name='%s_mn/compress' % self.name
        )

        """
        residual_filter
        """
        if self.add_residual and self._channels_in != self._channels_out:
            residual_filter = UtilityVariable.initialize_weight(
                [1,
                 1,
                 self._channels_in,
                 self._channels_out],
                l2_regular=self._l2_regular,
                name='%s_mn/residual' % self.name
            )
        else:
            residual_filter = None

        """
        bias
        """
        if self.add_bias:
            bias = UtilityVariable.initialize_bias(
                [self._channels_out],
                name='%s_mn/bias' % self.name
            )
        else:
            bias = None

        return dilatation_filter, \
               depthwise_filter, \
               compress_filter, \
               residual_filter, \
               bias

    def _calculate(self,
                   batch_input):
        """
        No activation function applied on output.
        :param batch_input:
        :return:
        """

        """
        dilate
        """
        if self.dilate_filter is not None:

            dilatation_o = tf.nn.conv2d(input=batch_input,
                                        filter=self.dilate_filter,
                                        strides=[1, 1, 1, 1],
                                        padding='SAME')

            if self._depth_active_func is not None:
                dilatation_o = self._dilate_active_func(
                    features=dilatation_o,
                    name='%s_mn/dilate_active' % self.name
                )
        else:
            dilatation_o = batch_input

        """
        depth-wise
        """
        convolution_o = tf.nn.depthwise_conv2d(input=dilatation_o,
                                               filter=self.depth_filter,
                                               strides=[1, self._stride, self._stride, 1],
                                               padding=self.padding)
        if self._depth_active_func is not None:
            convolution_o = self._depth_active_func(
                features=convolution_o,
                name='%s_mn/depth_active' % self.name
            )

        """
        compress
        """
        compress_o = tf.nn.conv2d(input=convolution_o,
                                  filter=self.compress_filter,
                                  strides=[1, 1, 1, 1],
                                  padding='SAME')

        """
        residual block
        """
        if self.add_residual is True:
            if self.residual_filter is not None:
                batch_input = tf.nn.conv2d(input=batch_input,
                                           filter=self.residual_filter,
                                           strides=[1, 1, 1, 1],
                                           padding='SAME')

            batch_output = tf.add(compress_o, batch_input)
        else:
            batch_output = compress_o

        """
        bias
        """
        if self.bias is not None:
            batch_output += self.bias

        return batch_output

    def get_features(self):
        """
        :return: image out
        """
        return self.features

    def get_variables(self, sess=None, save_dir=None):
        """
        :return: variable
        """
        if sess is None:
            return self.dilate_filter, \
                   self.depth_filter, \
                   self.compress_filter, \
                   self.residual_filter, \
                   self.bias
        else:
            dilate_filter = None if self.dilate_filter is None else sess.run(self.dilate_filter)
            depth_filter = None if self.depth_filter is None else sess.run(self.depth_filter)
            compress_filter = None if self.compress_filter is None else sess.run(self.compress_filter)
            residual_filter = None if self.residual_filter is None else sess.run(self.residual_filter)
            bias = None if self.bias is None else sess.run(self.bias)

            if save_dir is not None:
                if dilate_filter is not None:
                    shape = '[%d,%d,%d,%d]' % dilate_filter.shape
                    numpy.savetxt(fname='%s/mn-dilate-%s.txt' % (save_dir, shape),
                                  X=numpy.reshape(dilate_filter, [-1]),
                                  header='%s: dilatation filter' % MobileNet.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/mn-dilate-%s.npy' % (save_dir, shape),
                               arr=dilate_filter)

                if depth_filter is not None:
                    shape = '[%d,%d,%d,%d]' % depth_filter.shape
                    numpy.savetxt(fname='%s/mn-depthwise-%s.txt' % (save_dir, shape),
                                  X=numpy.reshape(depth_filter, [-1]),
                                  header='%s: depthwise filter' % MobileNet.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/mn-depthwise-%s.npy' % (save_dir, shape),
                               arr=depth_filter)

                if compress_filter is not None:
                    shape = '[%d,%d,%d,%d]' % compress_filter.shape
                    numpy.savetxt(fname='%s/mn-compress-%s.txt' % (save_dir, shape),
                                  X=numpy.reshape(compress_filter, [-1]),
                                  header='%s: compress filter' % MobileNet.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/mn-compress-%s.npy' % (save_dir, shape),
                               arr=compress_filter)

                if residual_filter is not None:
                    shape = '[%d,%d,%d,%d]' % residual_filter.shape
                    numpy.savetxt(fname='%s/mn-residual-%s.txt' % (save_dir, shape),
                                  X=numpy.reshape(residual_filter, [-1]),
                                  header='%s: residual filter' % MobileNet.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/mn-residual-%s.npy' % (save_dir, shape),
                               arr=residual_filter)

                if bias is not None:
                    shape = '[%d]' % bias.shape
                    numpy.savetxt(fname='%s/mn-bias-%s.txt' % (save_dir, shape),
                                  X=bias,
                                  header='%s: bias' % MobileNet.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/mn-bias-%s.npy' % (save_dir, shape),
                               arr=bias)

            return dilate_filter, \
                   depth_filter, \
                   compress_filter, \
                   residual_filter, \
                   bias

    def get_config(self):
        """
        export config as a list
        :return:
        """

        """
        multiplication calculation
        """
        multiplication_dilate, \
        multiplication_depth, \
        multiplication_compress, \
        multiplication_residual = self.get_multiplication_amount(height_in=self._height_in,
                                                                 width_in=self._width_in,
                                                                 dilate_number=self._dilate_number,
                                                                 channels_in=self._channels_in,
                                                                 channels_out=self._channels_out,
                                                                 filter_size=self._filter_size,
                                                                 stride=self._stride,
                                                                 add_residual=self.add_residual,
                                                                 padding=self.padding)

        dilate_shape = None if self.dilate_filter is None else self.dilate_filter.shape
        depth_shape = None if self.depth_filter is None else self.depth_filter.shape
        compress_shape = None if self.compress_filter is None else self.compress_filter.shape
        residual_shape = None if self.residual_filter is None else self.residual_filter.shape
        bias_shape = None if self.bias is None else self.bias.shape

        config = [
            '\n### %s\n' % self.name,
            '> MobileNet\n',
            '- filter size: %d\n' % self._filter_size,
            '- channels in: %d\n' % self._channels_in,
            '- channels out: %d\n' % self._channels_out,
            '- dilatation: %s\n' % self._dilate_number,
            '- dilate active function: %s\n' % self._dilate_active_func_name,
            '- depth-wise active function: %s\n' % self._depth_active_func_name,
            '- stride: %d\n' % self._stride,
            '- add residual: %s\n' % self.add_residual,
            '- add bias: %s\n' % self.add_bias,
            '- padding: %s\n' % self.padding,
            '- variables:\n',
            '   - dilatation: %s\n' % dilate_shape,
            '   - depth-wise: %s\n' % depth_shape,
            '   - compress: %s\n' % compress_shape,
            '   - residual: %s\n' % residual_shape,
            '   - bias: %s\n' % bias_shape,
            '- multiplicative amount: %d\n' % (multiplication_dilate
                                               + multiplication_depth
                                               + multiplication_compress
                                               + multiplication_residual),
            '   - dilatation: %d\n' % multiplication_dilate,
            '   - depth-wise: %d\n' % multiplication_depth,
            '   - compress: %d\n' % multiplication_compress,
            '   - residual: %d\n' % multiplication_residual
        ]

        return config

    @staticmethod
    def get_multiplication_amount(height_in,
                                  width_in,
                                  dilate_number,
                                  channels_in,
                                  channels_out,
                                  filter_size,
                                  stride,
                                  add_residual,
                                  padding):

        if height_in is None or width_in is None:
            return -1, -1, -1, -1

        else:
            if padding == MobileNet.VALID:
                height_out = round((height_in - filter_size + 1) / stride)
                width_out = round((width_in - filter_size + 1) / stride)
            elif padding == MobileNet.SAME:
                height_out = round(height_in / stride)
                width_out = round(width_in / stride)
            else:
                height_out = 0
                width_out = 0
                print('Error: '
                      '[%s.%s] '
                      'wrong padding mode.' % (MobileNet.__name__,
                                               MobileNet.__init__.__name__))
            if dilate_number is None:
                dilate = 0
                depth = height_out * width_out * filter_size * filter_size * channels_in
                compress = height_out * width_out * channels_in * channels_out
            else:
                dilate = height_in * width_in * channels_in * dilate_number
                depth = height_out * width_out * filter_size * filter_size * dilate_number
                compress = height_out * width_out * dilate_number * channels_out

            if add_residual and channels_in != channels_out:
                residual = height_in * width_out * channels_in * channels_out
            else:
                residual = 0

            return dilate, depth, compress, residual


if __name__ == '__main__':
    from easy_net_tf.utility.file import UtilityFile
    from pathlib import Path

    image = numpy.array([[[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]]],
                        dtype=numpy.float32)

    image_ph = tf.placeholder(dtype=tf.float32, shape=[None, None, None, 3])

    mn = MobileNet(batch_input=image_ph,
                   dilate_number=1,
                   filter_size=3,
                   channels_out=15,
                   dilate_active_func=tf.nn.relu6,
                   depth_active_func=tf.nn.leaky_relu,
                   stride=1,
                   add_residual=True,
                   add_bias=False,
                   padding=MobileNet.SAME,
                   name='l1')

    UtilityFile.save_str_list('test-mn.md', mn.get_config())
