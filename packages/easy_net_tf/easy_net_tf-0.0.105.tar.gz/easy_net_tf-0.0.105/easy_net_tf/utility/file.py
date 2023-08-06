import random
import os


class UtilityFile:
    @staticmethod
    def _line_generator(read_path):
        """
        get a line generator of a file
        :param read_path: string
        :return:
        """
        with open(read_path, 'r') as file:
            while True:
                line = file.readline()
                if line:
                    yield line
                else:
                    return

    @staticmethod
    def _line_shuffle(read_path):
        """
        first get all lines in file, then shuffle, finally save to file again.
        :param read_path: string
        :return:
        """
        # read
        with open(read_path, 'r') as file:
            info_list = file.readlines()

        # shuffle
        random.shuffle(info_list)

        # write
        with open(read_path, 'w') as file:
            for info in info_list:
                file.write(info)

    @staticmethod
    def get_file_list(directory, shuffle):
        """

        :param directory:
        :param shuffle:
        :return:
        """

        file_list = os.listdir(directory)

        if shuffle:
            random.shuffle(file_list)

        return file_list

    @staticmethod
    def get_line_generator(read_path,
                           shuffle):
        """

        :param read_path:
        :param shuffle: True: first shuffle and save, then return generator; False: return generator
        :return:
        """

        if shuffle:
            UtilityFile._line_shuffle(read_path)

        return UtilityFile._line_generator(read_path)

    @staticmethod
    def save_str_list(write_path,
                      info_list,
                      mode='w'):
        """
        save a list of info to a file
        :param write_path: string
        :param info_list: a list of info to save
        :param mode: file mode
        :return:
        """
        with open(write_path, mode) as file:
            for info in info_list:
                file.write(str(info))

    @staticmethod
    def count(count: dict = None,
              directory: str = None,
              sub_dir: bool = False):

        for root, batch_dir, batch_filename in os.walk(directory):
            for filename in batch_filename:
                suffix = os.path.splitext(filename)[1]
                if suffix in count:
                    count[suffix] += 1
                else:
                    count[suffix] = 1

            if sub_dir:
                for _dir in batch_dir:
                    count = UtilityFile.count(
                        count=count,
                        directory=root + '/' + _dir
                    )

        return count


if __name__ == '__main__':
    # UtilityFile.save_str_list(
    #     'test.txt',
    #     ['net',
    #      0.88,
    #      128,
    #      'hello',
    #      False,
    #      True,
    #      None]
    # )

    c_result = UtilityFile.count(
        count={},
        directory='/home/yehangyang/Documents/Gitlab/AI_database/cache/MTMN/human_face_4/O/datum/val/negative',
        sub_dir=True
    )

    for key, value in c_result.items():
        print('%s: %d' % (key, value))
