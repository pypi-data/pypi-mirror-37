import numpy
import cv2
import math

from easydict import EasyDict

from easy_net_tf.utility.file import UtilityFile


class UtilityBounding:
    CIRCLE = 'CIRCLE'
    RECTANGLE = 'RECTANGLE'

    @staticmethod
    def rectangle_2_square(batch_rectangle,
                           image_width,
                           image_height):
        """
        convert rectangles to square shape with avoiding exceeding original image by move bounding towards image
        :param batch_rectangle:
        :param image_width:
        :param image_height:
        :return:
        """

        if batch_rectangle is None:
            return None

        squares = numpy.copy(batch_rectangle)

        batch_height = batch_rectangle[:, 3] - batch_rectangle[:, 1] + 1
        batch_width = batch_rectangle[:, 2] - batch_rectangle[:, 0] + 1

        long_side = numpy.maximum(batch_height, batch_width)

        squares[:, 0] = batch_rectangle[:, 0] + 0.5 * batch_width - 0.5 * long_side
        squares[:, 1] = batch_rectangle[:, 1] + 0.5 * batch_height - 0.5 * long_side

        squares[:, 2] = squares[:, 0] + long_side - 1
        squares[:, 3] = squares[:, 1] + long_side - 1

        invalid_indexes = numpy.less(squares[:, 0], 0)
        squares[:, 2] = numpy.where(invalid_indexes,
                                    squares[:, 2] - squares[:, 0],
                                    squares[:, 2])
        squares[:, 0] = numpy.where(invalid_indexes,
                                    0,
                                    squares[:, 0])

        invalid_indexes = numpy.less(squares[:, 1], 0)
        squares[:, 3] = numpy.where(invalid_indexes,
                                    squares[:, 3] - squares[:, 1],
                                    squares[:, 3])
        squares[:, 1] = numpy.where(invalid_indexes,
                                    0,
                                    squares[:, 1])

        invalid_indexes = numpy.greater_equal(squares[:, 2], image_width)
        squares[:, 0] = numpy.where(invalid_indexes,
                                    squares[:, 0] - (squares[:, 2] - image_width + 1),
                                    squares[:, 0])
        squares[:, 2] = numpy.where(invalid_indexes,
                                    image_width - 1,
                                    squares[:, 2])

        invalid_indexes = numpy.greater_equal(squares[:, 3], image_height)
        squares[:, 1] = numpy.where(invalid_indexes,
                                    squares[:, 1] - (squares[:, 3] - image_height + 1),
                                    squares[:, 1])
        squares[:, 3] = numpy.where(invalid_indexes,
                                    image_height - 1,
                                    squares[:, 3])

        return squares

    @staticmethod
    def circle_2_square(batch_circle):
        """
        convert circle to square shape without avoiding exceeding original image by move bounding towards image
        :param batch_circle:
        :return:
        """

        batch_square = numpy.zeros(
            shape=(numpy.shape(batch_circle)[0], 4),
            dtype=numpy.int32
        )

        batch_square[:, 0] = batch_circle[:, 0] - batch_circle[:, 2]
        batch_square[:, 1] = batch_circle[:, 1] - batch_circle[:, 2]
        batch_square[:, 2] = batch_circle[:, 0] + batch_circle[:, 2]
        batch_square[:, 3] = batch_circle[:, 1] + batch_circle[:, 2]

        return batch_square

    @staticmethod
    def rectangle_offset_horizontally_flip(offset):
        """

        :param offset:[x1, y1, x2, y2]
        :return:
        """

        copy = offset.copy()
        copy[0], copy[2] = -copy[2], -copy[0]

        return copy

    @staticmethod
    def offset_horizontally_flip_circle(batch_offset):

        copy = numpy.copy(batch_offset)
        copy[:, 0] = -copy[:, 0]

        return copy

    @staticmethod
    def iou_circle(circle,
                   batch_circle):
        """
        calculate Intersection on Union of circle against to each of circles
        :param circle:
        :param batch_circle:
        :return: intersection on union
        """

        # prepare
        batch_circle = numpy.reshape(batch_circle, [-1, 3])
        pi = math.pi
        iou_list = list()

        # get distance between circles
        distances = numpy.sqrt(
            numpy.square(batch_circle[:, 0] - circle[0])
            + numpy.square(batch_circle[:, 1] - circle[1])
        )

        for index, circle_2 in enumerate(batch_circle):

            if circle_2[2] + circle[2] <= distances[index]:
                """
                separate
                """
                iou_list.append(0)

            elif numpy.abs(circle_2[2] - circle[2]) >= distances[index]:
                """
                include
                """
                if circle_2[2] > circle[2]:
                    g_radius = circle_2[2]
                    l_radius = circle[2]

                else:
                    g_radius = circle[2]
                    l_radius = circle_2[2]

                iou_list.append(
                    numpy.square(l_radius) / numpy.square(g_radius)
                )

            else:
                """
                intersect
                """
                # get rhombus_area
                perimeter = distances[index] + circle[2] + circle_2[2]

                rhombus_area = 2 * numpy.sqrt(
                    (perimeter / 2)
                    * (perimeter / 2 - circle_2[2])
                    * (perimeter / 2 - circle[2])
                    * (perimeter / 2 - distances[index])
                )

                # get sector area
                height = rhombus_area / distances[index]

                sector_area_1 = numpy.arcsin(height / circle_2[2]) * numpy.square(circle_2[2])
                sector_area_2 = numpy.arcsin(height / circle[2]) * numpy.square(circle[2])

                # get intersection
                inter_area = sector_area_1 + sector_area_2 - rhombus_area

                # get union
                union_area = pi * numpy.square(circle_2[2]) + pi * numpy.square(circle[2]) - inter_area

                # get iou
                iou = inter_area / union_area

                iou_list.append(iou)

        return iou_list

    @staticmethod
    def iou_circle2(circle,
                    batch_circle):
        """
        calculate as squares
        :param circle:
        :param batch_circle:
        :return:
        """

        batch_circle = numpy.reshape(batch_circle, [-1, 3])
        circle_area = (circle[2] * 2) * (circle[2] * 2)
        circles_area = (batch_circle[:, 2] * 2) * (batch_circle[:, 2] * 2)

        inter_x_1 = numpy.maximum(circle[0] - circle[2], batch_circle[:, 0] - batch_circle[:, 2])
        inter_y_1 = numpy.maximum(circle[1] - circle[2], batch_circle[:, 1] - batch_circle[:, 2])
        inter_x_2 = numpy.minimum(circle[0] + circle[2], batch_circle[:, 0] + batch_circle[:, 2])
        inter_y_2 = numpy.minimum(circle[1] + circle[2], batch_circle[:, 1] + batch_circle[:, 2])

        inter_w = numpy.maximum(0, inter_x_2 - inter_x_1 + 1)
        inter_h = numpy.maximum(0, inter_y_2 - inter_y_1 + 1)

        inter_area = inter_w * inter_h

        union = circle_area + circles_area - inter_area

        ious = inter_area / union

        return ious

    @staticmethod
    def iou_rectangle(rectangle,
                      batch_rectangle):
        """
        calculate Intersection on Union of rectangle against to each of rectangles
        :param rectangle:
        :param batch_rectangle:
        :return: ious, inter_area, rectangle_area, batch_rectangle_area
        """

        batch_rectangle = numpy.reshape(batch_rectangle, [-1, 4])

        rectangle_area = (rectangle[2] - rectangle[0] + 1) * (rectangle[3] - rectangle[1] + 1)
        batch_rectangle_area = (batch_rectangle[:, 2] - batch_rectangle[:, 0] + 1) * (
                batch_rectangle[:, 3] - batch_rectangle[:, 1] + 1)

        inter_x_1 = numpy.maximum(rectangle[0], batch_rectangle[:, 0])
        inter_y_1 = numpy.maximum(rectangle[1], batch_rectangle[:, 1])
        inter_x_2 = numpy.minimum(rectangle[2], batch_rectangle[:, 2])
        inter_y_2 = numpy.minimum(rectangle[3], batch_rectangle[:, 3])

        inter_w = numpy.maximum(0, inter_x_2 - inter_x_1 + 1)
        inter_h = numpy.maximum(0, inter_y_2 - inter_y_1 + 1)

        inter_area = inter_w * inter_h
        union = rectangle_area + batch_rectangle_area - inter_area  # + 10e-10

        ious = inter_area / union

        return ious, inter_area, rectangle_area, batch_rectangle_area

    UNION = 'Union'
    MIN = 'Minimum'

    @staticmethod
    def nms_rectangle(batch_rectangle,
                      batch_score,
                      threshold,
                      mode='Union'):
        """
        non maximum suppression
        :param batch_rectangle:
        :param batch_score:
        :param threshold:
        :param mode:
        :return: kept indexes
        """

        x_1 = batch_rectangle[:, 0]
        y_1 = batch_rectangle[:, 1]
        x_2 = batch_rectangle[:, 2]
        y_2 = batch_rectangle[:, 3]

        batch_rectangle_area = (x_2 - x_1 + 1) * (y_2 - y_1 + 1)
        increase_order_indexes = numpy.argsort(-batch_score, axis=0)

        kept_indexes = list()

        while numpy.size(increase_order_indexes) > 0:
            index = increase_order_indexes[0]
            other_indexes = increase_order_indexes[1:]

            kept_indexes.append(index)

            if numpy.size(other_indexes) <= 0:
                break

            # intersection over union
            inter_x_1 = numpy.maximum(x_1[index], x_1[other_indexes])
            inter_y_1 = numpy.maximum(y_1[index], y_1[other_indexes])
            inter_x_2 = numpy.minimum(x_2[index], x_2[other_indexes])
            inter_y_2 = numpy.minimum(y_2[index], y_2[other_indexes])

            inter_width = numpy.maximum(inter_x_2 - inter_x_1 + 1, 0.0)
            inter_height = numpy.maximum(inter_y_2 - inter_y_1 + 1, 0.0)

            inter_area = inter_width * inter_height

            if mode == UtilityBounding.UNION:
                ious = inter_area / \
                       (batch_rectangle_area[index]
                        + batch_rectangle_area[other_indexes]
                        - inter_area)
            elif mode == UtilityBounding.MIN:
                ious = inter_area / \
                       numpy.minimum(
                           batch_rectangle_area[index],
                           batch_rectangle_area[other_indexes]
                       )
            else:
                print('Error: '
                      '[%s.%s] '
                      'mns mode can only be ''%s'' or ''%s''.'
                      % (UtilityBounding.__name__,
                         UtilityBounding.nms_rectangle.__name__,
                         UtilityBounding.MIN,
                         UtilityBounding.UNION))
                return None

            mask_index = numpy.where(ious <= threshold)[0]
            if numpy.size(mask_index) <= 0:
                break
            increase_order_indexes = other_indexes[mask_index]

        return kept_indexes

    @staticmethod
    def nms_circle2(batch_circle,
                    batch_score,
                    threshold,
                    mode='Union'):
        """
        calculate iou in a square way
        non maximum suppression
        :param batch_circle:
        :param batch_score:
        :param threshold:
        :param mode:
        :return: kept indexes
        """

        x_1 = batch_circle[:, 0] - batch_circle[:, 2]
        y_1 = batch_circle[:, 1] - batch_circle[:, 2]
        x_2 = batch_circle[:, 0] + batch_circle[:, 2]
        y_2 = batch_circle[:, 1] + batch_circle[:, 2]

        batch_rectangle_area = (x_2 - x_1 + 1) * (y_2 - y_1 + 1)
        increase_order_indexes = numpy.argsort(-batch_score, axis=0)

        kept_indexes = list()

        while numpy.size(increase_order_indexes) > 0:
            index = increase_order_indexes[0]
            other_indexes = increase_order_indexes[1:]

            kept_indexes.append(index)

            if numpy.size(other_indexes) <= 0:
                break

            # intersection over union
            inter_x_1 = numpy.maximum(x_1[index], x_1[other_indexes])
            inter_y_1 = numpy.maximum(y_1[index], y_1[other_indexes])
            inter_x_2 = numpy.minimum(x_2[index], x_2[other_indexes])
            inter_y_2 = numpy.minimum(y_2[index], y_2[other_indexes])

            inter_width = numpy.maximum(inter_x_2 - inter_x_1 + 1, 0.0)
            inter_height = numpy.maximum(inter_y_2 - inter_y_1 + 1, 0.0)

            inter_area = inter_width * inter_height

            if mode == UtilityBounding.UNION:
                ious = inter_area / \
                       (batch_rectangle_area[index]
                        + batch_rectangle_area[other_indexes]
                        - inter_area)
            elif mode == UtilityBounding.MIN:
                ious = inter_area / \
                       numpy.minimum(
                           batch_rectangle_area[index],
                           batch_rectangle_area[other_indexes]
                       )
            else:
                print('Error: '
                      '[%s.%s] '
                      'mns mode can only be ''%s'' or ''%s''.'
                      % (UtilityBounding.__name__,
                         UtilityBounding.nms_rectangle.__name__,
                         UtilityBounding.MIN,
                         UtilityBounding.UNION))
                return None

            mask_index = numpy.where(ious <= threshold)[0]
            if numpy.size(mask_index) <= 0:
                break
            increase_order_indexes = other_indexes[mask_index]

        return kept_indexes

    @staticmethod
    def normalize_circle(circle, random):
        normal_offset = [
            (circle[0] - random[0]) / random[2],
            (circle[1] - random[1]) / random[2],
            (circle[2] - random[2]) / random[2]
        ]

        return normal_offset

    @staticmethod
    def normalize_rectangle(rectangle, random):

        if random[2] - random[0] == random[3] - random[1]:
            size = random[2] - random[0] + 1
        else:
            return False

        normal_offset = [
            (rectangle[0] - random[0]) / size,
            (rectangle[1] - random[1]) / size,
            (rectangle[2] - random[2]) / size,
            (rectangle[3] - random[3]) / size
        ]

        return normal_offset

    @staticmethod
    def regress_circle(batch_circle,
                       batch_normal_offset):
        """
        calibrate rectangles by adding offsets
        :param batch_circle:
        :param batch_normal_offset:
        :return:
        """

        regress_batch_circle = numpy.copy(batch_normal_offset)

        for circle, regress_circle in zip(batch_circle, regress_batch_circle):
            regress_circle *= circle[2]
            regress_circle += circle

        return regress_batch_circle

    @staticmethod
    def regress_rectangle(batch_rectangle,
                          batch_normal_offset):
        """
        calibrate rectangles by adding offsets
        :param batch_rectangle:
        :param batch_normal_offset:
        :return:
        """

        regress_batch_rectangle = numpy.copy(batch_normal_offset)

        for rectangle, regress_rectangle in zip(batch_rectangle, regress_batch_rectangle):
            width = rectangle[2] - rectangle[0] + 1
            height = rectangle[3] - rectangle[1] + 1

            regress_rectangle = numpy.reshape(
                a=regress_rectangle,
                newshape=[-1, 2]
            )

            regress_rectangle[:, 0] *= width
            regress_rectangle[:, 1] *= height

            regress_rectangle = numpy.reshape(
                a=regress_rectangle,
                newshape=[-1]
            )

            regress_rectangle += rectangle

        return regress_batch_rectangle

    @staticmethod
    def wilder_rectangle_2_circle(read_path,
                                  write_path,
                                  log=False):
        """

        :param read_path: str
        :param write_path: str
        :param log:
        :return:
        """
        info_generator = UtilityFile.get_line_generator(
            read_path=read_path,
            shuffle=False
        )

        sample_index = 0
        with open(write_path, 'w') as file:
            while True:
                if log:
                    sample_index += 1
                    print('Log: '
                          '[%s.%s] '
                          'sample: %d'
                          % (UtilityBounding.__name__,
                             UtilityBounding.wilder_rectangle_2_circle.__name__,
                             sample_index)
                          )
                try:
                    """
                    get info
                    """
                    info = info_generator.__next__().strip().split(' ')

                    image_path = info.pop(0)

                    batch_rectangle = numpy.reshape(
                        numpy.array(info, dtype=numpy.float32),
                        [-1, 4]
                    )

                    """
                    convert to circle
                    """
                    circle_list = list()
                    for rectangle in batch_rectangle:
                        center_x = (rectangle[0] + rectangle[2]) / 2
                        center_y = (rectangle[1] + rectangle[3]) / 2
                        radius = numpy.sqrt(
                            numpy.square(rectangle[0] - rectangle[2])
                            + numpy.square(rectangle[1] - rectangle[3])
                        ) / 2

                        circle = [center_x, center_y, radius]
                        circle_list.append(circle)

                    """
                    save to file
                    """
                    circles = numpy.reshape(
                        numpy.array(circle_list),
                        [-1]
                    )

                    new_info = image_path + ' ' + ' '.join(map(str, circles)) + '\n'
                    file.write(new_info)

                except StopIteration:
                    break
        return

    @staticmethod
    def verify_circle(read_path,
                      image_dir,
                      delay):
        """

        :param read_path: circle bounding label file path
        :param image_dir: image folder directory
        :param delay:
        :return:
        """
        info_generator = UtilityFile.get_line_generator(
            read_path=read_path,
            shuffle=False
        )

        while True:
            try:
                info = info_generator.__next__().strip().split(' ')
                image_name = '%s.jpg' % info.pop(0)
                image_path = image_dir + '/' + image_name

                image = cv2.imread(image_path)

                circle_list = numpy.reshape(
                    list(map(float, info)),
                    [-1, 3]
                )

                for circle in circle_list:
                    circle = numpy.round(circle)
                    x = int(circle[0])
                    y = int(circle[1])
                    radius = int(circle[2])

                    cv2.circle(img=image,
                               center=(x, y),
                               radius=radius,
                               color=(0, 255, 0),
                               thickness=2)

                cv2.imshow('circle bounding', image)
                cv2.waitKey(delay)

            except StopIteration:
                break


if __name__ == '__main__':
    UtilityBounding.wilder_rectangle_2_circle(
        read_path='/home/yehangyang/Documents/Gitlab/AI_database/wider_face/val/labels.txt',
        write_path='/home/yehangyang/Documents/Gitlab/AI_database/wider_face/val/labels-c.txt',
        log=True
    )
