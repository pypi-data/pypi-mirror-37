import time
import numpy
import cv2

import inspect

from easy_net_tf.utility.image import UtilityImage


class UtilityLog:
    ERROR = 'Error:   '
    LOG = 'Log:     '
    WARNING = 'Warning: '

    @staticmethod
    def text(content,
             name,
             tag,
             option):
        """

        :param content:
        :param name:
        :param tag: 'Error', 'Log', 'Warning'
        :param option: True: print content;
                    False: disabled;
                    string: save in it as file
        :return:
        """
        if option:
            content = '%s%s | [%s.%s] %s' % \
                      (tag,
                       time.strftime('%Y-%m-%d-%H:%M:%S'),
                       name,
                       inspect.stack()[1][3],
                       content)
            print(content)

            if type(option) is str and option is not '':
                with open(option, 'a') as file:
                    file.write(content + '\n')

        return

    @staticmethod
    def image(image,
              batch_rectangle=(
                      [
                          [1, 1, 1, 1],
                          [2, 2, 2, 2]
                      ],
                      (255, 0, 0)
              ),
              batch_point=(
                      [
                          [1, 1],
                          [2, 2]
                      ],
                      (0, 255, 0)
              ),
              text=(
                      'content',
                      (0, 0, 255)
              ),
              hint='window name',
              delay=0):

        if delay is None:
            return

        copy = numpy.copy(image)

        copy = UtilityImage.draw_rectangle(
            image=copy,
            batch_rectangle=batch_rectangle[0],
            color=batch_rectangle[1],
        )

        if batch_point is not None:
            copy = UtilityImage.draw_point(
                image=copy,
                batch_point=batch_point[0],
                color=batch_point[1]
            )

        copy = cv2.putText(
            img=copy,
            text=text[0],
            org=(0, round(image.shape[0] / 2)),
            fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            fontScale=3,
            color=text[1]
        )

        cv2.imshow(winname=hint, mat=copy)
        cv2.waitKey(delay)

        return
