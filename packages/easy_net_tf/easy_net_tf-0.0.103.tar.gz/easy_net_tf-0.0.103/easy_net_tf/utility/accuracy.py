import tensorflow as tf


class UtilityAccuracy:

    @staticmethod
    def count(predict, truth):
        """
        binary classification only now
        :param predict:
        :param truth:
        :return:
        """

        predict = tf.cast(predict, dtype=tf.int32)

        truth = tf.cast(
            tf.reshape(truth, [-1]),
            dtype=tf.int32
        )

        mask_ones = tf.ones_like(truth, dtype=tf.int32)
        mask_zeros = tf.zeros_like(truth, dtype=tf.int32)

        tp = tf.reduce_sum(
            tf.cast(
                tf.logical_and(
                    tf.equal(truth, mask_ones),
                    tf.equal(predict, mask_ones)
                ),
                dtype=tf.float32))

        tn = tf.reduce_sum(
            tf.cast(
                tf.logical_and(
                    tf.equal(truth, mask_zeros),
                    tf.equal(predict, mask_zeros)
                ),
                dtype=tf.float32
            )
        )

        fp = tf.reduce_sum(
            tf.cast(
                tf.logical_and(
                    tf.equal(truth, mask_zeros),
                    tf.equal(predict, mask_ones)
                ),
                dtype=tf.float32
            )
        )

        fn = tf.reduce_sum(
            tf.cast(
                tf.logical_and(
                    tf.equal(truth, mask_ones),
                    tf.equal(predict, mask_zeros)
                ),
                dtype=tf.float32
            )
        )

        tf.summary.scalar(name='TP', tensor=tp)
        tf.summary.scalar(name='TN', tensor=tn)
        tf.summary.scalar(name='FP', tensor=fp)
        tf.summary.scalar(name='FN', tensor=fn)
        tf.summary.scalar(name='total', tensor=tp + tn + fp + fn)

        return tp, tn, fp, fn

    @staticmethod
    def recall(tp, fn):
        result = tp / (tp + fn)
        tf.summary.scalar(name='recall', tensor=result)
        return result

    @staticmethod
    def accuracy(tp, tn, fp, fn):
        result = (tp + tn) / (tp + tn + fp + fn)
        tf.summary.scalar(name='accuracy', tensor=result)
        return result

    @staticmethod
    def precision(tp, fp):
        result = tp / (tp + fp)
        tf.summary.scalar(name='precision', tensor=result)
        return result

    @staticmethod
    def f1_score(tp, fp, fn):
        result = 2 * tp / (2 * tp + fp + fn)
        tf.summary.scalar(name='f1_score', tensor=result)
        return result
