import numpy

from easy_net_tf.utility.image import UtilityImage


class UtilitySlideWindow:

    @staticmethod
    def slide_window(image, window_size, stride):
        image_height, image_width, channels = image.shape

        x_1 = 0
        y_1 = 0
        x_2 = window_size - 1
        y_2 = window_size - 1

        if x_2 >= image_width or y_2 >= image_height:
            return None, None

        box_list = list()
        image_list = list()

        while y_2 < image_height - 1:

            while x_2 < image_width - 1:
                sub_image = UtilityImage.cut_out_rectangle(image=image,
                                                           rectangle=[x_1, y_1, x_2, y_2])

                box_list.append([x_1, y_1, x_2, y_2])
                image_list.append(sub_image)

                # go to next column
                x_1 += stride
                x_2 += stride

            # the last column
            x_1 = image_width - window_size
            x_2 = image_width - 1

            sub_image = UtilityImage.cut_out_rectangle(image=image,
                                                       rectangle=[x_1, y_1, x_2, y_2])
            box_list.append([x_1, y_1, x_2, y_2])
            image_list.append(sub_image)

            # back to the first column
            x_1 = 0
            x_2 = window_size - 1
            # go to next row
            y_1 += stride
            y_2 += stride

        # the last row
        y_1 = image_height - window_size
        y_2 = image_height - 1
        while x_2 < image_width - 1:
            sub_image = UtilityImage.cut_out_rectangle(image=image,
                                                       rectangle=[x_1, y_1, x_2, y_2])
            box_list.append([x_1, y_1, x_2, y_2])
            image_list.append(sub_image)

            # go to next column
            x_1 += stride
            x_2 += stride

        # the last column
        x_1 = image_width - window_size
        x_2 = image_width - 1

        sub_image = UtilityImage.cut_out_rectangle(image=image,
                                                   rectangle=[x_1, y_1, x_2, y_2])
        box_list.append([x_1, y_1, x_2, y_2])
        image_list.append(sub_image)

        images = None
        for image in image_list:

            image = numpy.reshape(image, [1, window_size, window_size, channels])
            if images is None:
                images = image
            else:
                images = numpy.vstack((images, image))

        boxes = numpy.array(box_list)

        return images, boxes
