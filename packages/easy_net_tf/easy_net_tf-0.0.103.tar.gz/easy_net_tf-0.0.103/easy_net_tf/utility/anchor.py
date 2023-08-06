import numpy


class UtilityAnchor:
    @staticmethod
    def generate_anchors(map_height,
                         map_width,
                         stride,
                         template,
                         anchor_number):
        """
        generate anchors centre from map
        :param map_height:
        :param map_width:
        :param stride:
        :return:
        """
        map_x = numpy.arange(start=0,
                             stop=map_width,
                             dtype=numpy.float32)
        anchors_centre_x = map_x * stride + int(stride / 2)

        map_y = numpy.arange(start=0,
                             stop=map_height,
                             dtype=numpy.float32)

        anchors_centre_y = map_y * stride + int(stride / 2)

        anchors_centre_x, anchors_centre_y = numpy.meshgrid(anchors_centre_x,
                                                            anchors_centre_y)

        anchors_centre = numpy.transpose(numpy.vstack((numpy.ravel(anchors_centre_x),
                                                       numpy.ravel(anchors_centre_y),
                                                       numpy.ravel(anchors_centre_x),
                                                       numpy.ravel(anchors_centre_y))))

        anchors_centre = numpy.repeat(anchors_centre, anchor_number, axis=0)
        anchors_centre = numpy.reshape(anchors_centre, [map_height, map_width, anchor_number, 4])

        anchors = template + anchors_centre

        return anchors

    @staticmethod
    def generate_template(min_face,
                          max_face,
                          positive_border):
        width_list = list()
        face_size = min_face
        width_list.append(face_size)
        while face_size < max_face * positive_border:
            face_size /= (positive_border * 1.025)
            width_list.append(round(face_size))

        width_list.append(max_face)

        widths = numpy.array(width_list, dtype=numpy.int32)

        anchors_x_1 = numpy.round(-(widths - 1) / 2)
        anchors_y_1 = numpy.round(-(widths - 1) / 2)
        anchors_x_2 = widths + anchors_x_1 - 1
        anchors_y_2 = widths + anchors_y_1 - 1

        template = numpy.transpose(numpy.array([anchors_x_1,
                                                anchors_y_1,
                                                anchors_x_2,
                                                anchors_y_2],
                                               dtype=numpy.int32))
        total = len(width_list)

        return template, total, widths, widths
