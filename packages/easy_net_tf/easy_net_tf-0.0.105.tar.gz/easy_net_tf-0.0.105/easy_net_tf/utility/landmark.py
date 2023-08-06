import numpy
import cv2
import math

from easy_net_tf.utility.file import UtilityFile
from easy_net_tf.utility.image import UtilityImage
from easy_net_tf.utility.log import UtilityLog


class UtilityLandmark:

    @staticmethod
    def normalize_circle(landmark, batch_circle):
        """

        :param batch_circle: [batch, 3]
        :param landmark: an EasyDict object
                        landmark['left']
                        landmark['center']
                        landmark['right']
        :return:
        """

        batch_normal_landmark = list()
        for circle in batch_circle:

            normal_landmark = dict()
            normal_landmark['left'] = list()
            normal_landmark['center'] = list()
            normal_landmark['right'] = list()

            # left
            for x, y in numpy.reshape(
                    a=landmark['left'],
                    newshape=[-1, 2]
            ):
                normal_landmark['left'].append(
                    [(x - circle[0] + circle[2]) / (circle[2] * 2 + 1),
                     (y - circle[1] + circle[2]) / (circle[2] * 2 + 1)]
                )

            # center
            for x, y in numpy.reshape(
                    a=landmark['center'],
                    newshape=[-1, 2]
            ):
                normal_landmark['center'].append(
                    [(x - circle[0] + circle[2]) / (circle[2] * 2 + 1),
                     (y - circle[1] + circle[2]) / (circle[2] * 2 + 1)])

            # right
            for x, y in numpy.reshape(
                    a=landmark['right'],
                    newshape=[-1, 2]
            ):
                normal_landmark['right'].append(
                    [(x - circle[0] + circle[2]) / (circle[2] * 2 + 1),
                     (y - circle[1] + circle[2]) / (circle[2] * 2 + 1)])

            batch_normal_landmark.append(
                normal_landmark
            )

        return batch_normal_landmark

    @staticmethod
    def normalize_rectangle(landmark, batch_rectangle):
        """

        :param batch_rectangle: [batch, 4]
        :param landmark: an EasyDict object
                        landmark['left']
                        landmark['center']
                        landmark['right']
        :return:
        """

        batch_normal_landmark = list()
        for rectangle in batch_rectangle:

            normal_landmark = dict()
            normal_landmark['left'] = list()
            normal_landmark['center'] = list()
            normal_landmark['right'] = list()

            # left
            for x, y in numpy.reshape(
                    a=landmark['left'],
                    newshape=[-1, 2]
            ):
                normal_landmark['left'].append(
                    [(x - rectangle[0]) / (rectangle[2] - rectangle[0] + 1),
                     (y - rectangle[1]) / (rectangle[3] - rectangle[1] + 1)]
                )

            # center
            for x, y in numpy.reshape(
                    a=landmark['center'],
                    newshape=[-1, 2]
            ):
                normal_landmark['center'].append(
                    [(x - rectangle[0]) / (rectangle[2] - rectangle[0] + 1),
                     (y - rectangle[1]) / (rectangle[3] - rectangle[1] + 1)]
                )

            # right
            for x, y in numpy.reshape(
                    a=landmark['right'],
                    newshape=[-1, 2]
            ):
                normal_landmark['right'].append(
                    [(x - rectangle[0]) / (rectangle[2] - rectangle[0] + 1),
                     (y - rectangle[1]) / (rectangle[3] - rectangle[1] + 1)]
                )

            batch_normal_landmark.append(
                normal_landmark
            )

        return batch_normal_landmark

    @staticmethod
    def regress_circle(batch_circle,
                       batch_normal_landmark):
        """
        calibrate landmarks to real scale
        :param batch_circle: [batch, 3]
        :param batch_normal_landmark: [batch, n]
        :return:
        """

        copy_batch_landmark = numpy.copy(batch_normal_landmark)

        for landmark, circle in zip(copy_batch_landmark, batch_circle):

            size = circle[2] * 2

            for _, point in enumerate(numpy.reshape(
                    a=landmark,
                    newshape=[-1, 2]
            )):
                point[0] *= size
                point[0] += (circle[0] - circle[2])

                point[1] *= size
                point[1] += (circle[1] - circle[2])

        return copy_batch_landmark

    @staticmethod
    def regress_rectangle(batch_rectangle,
                          batch_normal_landmark):
        """
        calibrate landmarks to real scale
        :param batch_rectangle: [batch, 4]
        :param batch_normal_landmark: [batch, 10]
        :return:
        """

        copy_batch_landmark = numpy.copy(batch_normal_landmark)

        for landmark, rectangle in zip(copy_batch_landmark, batch_rectangle):

            width = rectangle[2] - rectangle[0] + 1
            height = rectangle[3] - rectangle[1] + 1

            for _, point in enumerate(numpy.reshape(
                    a=landmark,
                    newshape=[-1, 2]
            )):
                point[0] *= width
                point[0] += rectangle[0]

                point[1] *= height
                point[1] += rectangle[1]

        return copy_batch_landmark

    @staticmethod
    def align_face(image, landmarks, template):
        image_height, image_width, _ = image.shape

        landmarks = numpy.reshape(landmarks, [-1, 2])
        template = numpy.reshape(template, [-1, 2])

        # maybe it is unnecessary, wait for proving!!!
        for index, _ in enumerate(landmarks):
            landmarks[index][0] *= image_width
            landmarks[index][1] *= image_height

            template[index][0] *= image_width
            template[index][1] *= image_height

        mat = cv2.estimateRigidTransform(src=landmarks,
                                         dst=template,
                                         fullAffine=True)

        align_image = cv2.warpAffine(src=image,
                                     M=mat,
                                     dsize=(image_height, image_width))

        return align_image

    @staticmethod
    def horizontally_flip(batch_normal_landmark):

        batch_normal_landmark_flip = list()

        for normal_landmark in batch_normal_landmark:
            normal_landmark_flip = dict()

            # left
            copy = numpy.copy(normal_landmark['left'])
            copy = numpy.reshape(
                a=copy,
                newshape=[-1, 2]
            )
            copy[:, 0] = 1 - copy[:, 0]
            normal_landmark_flip['right'] = copy

            # center
            copy = numpy.copy(normal_landmark['center'])
            copy = numpy.reshape(
                a=copy,
                newshape=[-1, 2]
            )
            copy[:, 0] = 1 - copy[:, 0]
            normal_landmark_flip['center'] = copy

            # right
            copy = numpy.copy(normal_landmark['right'])
            copy = numpy.reshape(
                a=copy,
                newshape=[-1, 2]
            )
            copy[:, 0] = 1 - copy[:, 0]
            normal_landmark_flip['left'] = copy

            batch_normal_landmark_flip.append(
                normal_landmark_flip
            )

        return batch_normal_landmark_flip

    @staticmethod
    def _point_rotate(batch_point, center, angle):
        """

        :param batch_point: shape: [ 10 ]
        :param center:
        :param angle:
        :return:
        """

        copy = batch_point.copy()
        copy = numpy.reshape(
            numpy.array(copy,
                        dtype=numpy.float32),
            [-1, 2]
        )
        rotate_mat = cv2.getRotationMatrix2D(center, angle, 1)

        batch_point_out = list()
        for x, y in copy:
            batch_point_out.append(rotate_mat[0][0] * x
                                   + rotate_mat[0][1] * y
                                   + rotate_mat[0][2])
            batch_point_out.append(rotate_mat[1][0] * x
                                   + rotate_mat[1][1] * y
                                   + rotate_mat[1][2])

        return batch_point_out

    @staticmethod
    def rotate(landmark, center, angle):
        copy = landmark.copy()

        # left
        copy['left'] = UtilityLandmark._point_rotate(
            batch_point=copy['left'],
            center=center,
            angle=angle
        )
        # center
        copy['center'] = UtilityLandmark._point_rotate(
            batch_point=copy['center'],
            center=center,
            angle=angle
        )
        # right
        copy['right'] = UtilityLandmark._point_rotate(
            batch_point=copy['right'],
            center=center,
            angle=angle
        )

        return copy

    @staticmethod
    def for_save(batch_landmark):
        batch_landmark_save = list()
        for landmark in batch_landmark:
            # left
            batch_landmark_save.extend(
                landmark['left']
            )
            # center
            batch_landmark_save.extend(
                landmark['center']
            )
            # right
            batch_landmark_save.extend(
                landmark['right']
            )
        return batch_landmark_save

    @staticmethod
    def mmlab_2_circle(read_path,
                       write_path,
                       log=False):
        info_generator = UtilityFile.get_line_generator(
            read_path=read_path,
            shuffle=False
        )

        sample_index = 0
        with open(write_path, 'w') as file:
            while True:

                UtilityLog.text(
                    content='sample: %d' % sample_index,
                    name=UtilityLandmark.__name__,
                    tag=UtilityLog.LOG,
                    option=log
                )
                try:
                    info = info_generator.__next__().strip().split(' ')
                    image_path = info.pop(0)
                    x_1 = int(info.pop(0))
                    x_2 = int(info.pop(0))
                    y_1 = int(info.pop(0))
                    y_2 = int(info.pop(0))

                    circle = [(x_1 + x_2) / 2,
                              (y_1 + y_2) / 2,
                              math.sqrt(
                                  math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2)
                              ) / 2]

                    new_info = image_path + ';' \
                               + ' '.join(map(str, circle)) + ';' \
                               + ' '.join(map(str, info)) + '\n'

                    file.write(new_info)

                except StopIteration:
                    break

        return

    @staticmethod
    def verify_mmlab(read_path,
                     image_dir,
                     delay=500,
                     log=False):

        """
        verify and show original label
        :param read_path:
        :param image_dir:
        :param delay:
        :param log:
        :return:
        """
        info_generator = UtilityFile.get_line_generator(
            read_path=read_path,
            shuffle=False
        )

        sample_index = 0

        while True:
            if log:
                sample_index += 1
                print('Log: '
                      '[%s.%s] '
                      'sample: %d' % (UtilityLandmark.__name__,
                                      UtilityLandmark.mmlab_2_circle.__name__,
                                      sample_index)
                      )
            try:
                info = info_generator.__next__().strip().split(' ')
                image_path = info.pop(0)
                image = cv2.imread(image_dir + '/' + image_path)

                x_1 = int(info.pop(0))
                x_2 = int(info.pop(0))
                y_1 = int(info.pop(0))
                y_2 = int(info.pop(0))

                image = UtilityImage.draw_rectangle(image=image,
                                                    batch_rectangle=[[x_1, y_1, x_2, y_2]],
                                                    color=(0, 255, 0))

                landmark = numpy.reshape(
                    a=numpy.array(list(map(float, info)), dtype=numpy.int32),
                    newshape=[-1, 2]
                )
                image = UtilityImage.draw_point(image=image,
                                                batch_point=landmark,
                                                color=(0, 255, 0))

                cv2.imshow('Original Landmark verify',
                           image)
                cv2.waitKey(delay)
            except StopIteration:
                break

        return

    @staticmethod
    def verify_circle(read_path,
                      image_dir,
                      delay=500,
                      log=False):
        """
        verify circle format label
        :param read_path:
        :param image_dir:
        :param delay:
        :param log:
        :return:
        """
        info_generator = UtilityFile.get_line_generator(
            read_path=read_path,
            shuffle=False
        )

        sample_index = 0

        while True:
            if log:
                sample_index += 1
                print('Log: '
                      '[%s.%s] '
                      'sample: %d' % (UtilityLandmark.__name__,
                                      UtilityLandmark.mmlab_2_circle.__name__,
                                      sample_index)
                      )
            try:
                info = info_generator.__next__().strip().split(';')
                image_path = info.pop(0)
                image = cv2.imread(image_dir + '/' + image_path)

                circle = list(map(float, info.pop(0).split(' ')))

                image = UtilityImage.draw_circle(image=image,
                                                 batch_circle=[circle])

                landmark = numpy.reshape(
                    a=numpy.array(list(map(float, info.pop(0).split(' '))), dtype=numpy.int32),
                    newshape=[-1, 2]
                )
                image = UtilityImage.draw_point(image=image,
                                                batch_point=landmark,
                                                color=(0, 255, 0))

                cv2.imshow('Original Landmark verify',
                           image)
                cv2.waitKey(delay)
            except StopIteration:
                break

        return


if __name__ == '__main__':
    UtilityLandmark.mmlab_2_circle(
        read_path='/home/yehangyang/Documents/Gitlab/AI_database/mmlab/data_set/train/labels.txt',
        write_path='/home/yehangyang/Documents/Gitlab/AI_database/mmlab/data_set/train/labels-c.txt',
        log=True
    )

    # UtilityLandmark.verify_mmlab(
    #     read_path='/home/yehangyang/Documents/Gitlab/AI_database/mmlab/data_set/train/trainImageList.txt',
    #     image_dir='/home/yehangyang/Documents/Gitlab/AI_database/mmlab/data_set/image',
    #     log=True
    # )

    # UtilityLandmark.verify_circle(
    #     read_path='/home/yehangyang/Documents/Gitlab/AI_database/mmlab/data_set/train/labels-c.txt',
    #     image_dir='/home/yehangyang/Documents/Gitlab/AI_database/mmlab/data_set/image',
    #     log=True
    # )
