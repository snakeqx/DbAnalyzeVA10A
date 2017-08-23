# -*- coding:utf-8 -*-
import logging
import os


class DirectoryHandler:
    """
    The class will iterate the input directory to find target database file.
    And store each found database file full path in a list of string "Database_File_Path"
    """
    Database_File_Path = []
    Target_To_Find = "report.db"

    def __init__(self, input_directory, target_to_find):
        """
        :param input_directory:
        :param target_to_find: target database file name
        """
        if input_directory is not None:
            if os.path.isdir(input_directory):
                logging.debug(r"Input is a folder which is correct.")
            else:
                logging.error(r"Input is not a folder, please double check!")
                return
        self.Target_To_Find = target_to_find
        logging.debug("The target is: " + str(self.Target_To_Find))
        self.list_files(input_directory)
        self.save_to_file()

    def save_to_file(self):
        file_object = open(r'./target_directory.ini', 'w')
        sample_list = self.Database_File_Path.copy()
        sample_list = [line+'\n' for line in sample_list]
        for _path in sample_list:
            file_object.writelines(str(_path))
        file_object.close()

    def list_files(self, input_directory):
        """
        :param input_directory:
        :return: no return. Directly write all target files found in Database_File_Path
        """
        try:
            dir_list = os.listdir(input_directory)
            for dl in dir_list:
                full_dl = os.path.join(input_directory, dl)
                if os.path.isfile(full_dl):
                    # judge if hitting target
                    if os.path.basename(full_dl) == self.Target_To_Find:
                        self.Database_File_Path.append(os.path.abspath(full_dl))
                        logging.info("Target found: " + str(os.path.abspath(full_dl)))
                        return
                    else:
                        logging.info(str(os.path.abspath(full_dl)))
                else:
                    self.list_files(full_dl)
        except Exception as e:
            logging.error(str(e))
            return


if __name__ == '__main__':
    print("please do not use it individually.")
    # below codes for debug
    # define the logging config, output in file
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=r'./DirectoryHandler.log',
                        filemode='w')
    # define a stream that will show log level > Warning on screen also
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    a = DirectoryHandler("Z:\\", "report.db")

