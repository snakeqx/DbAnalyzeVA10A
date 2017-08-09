import logging
import os
import sys

from DatabaseHandler import DatabaseHandler
from DirectoryHandler import DirectoryHandler
from EnumFunctionTable import StringResultTable, StringFunctionTables

# define the logging config, output in file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=r'./main.log',
                    filemode='w')
# define a stream that will show log level > Warning on screen also
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def initial_table_header():
    file_object = open(r'./query_result.csv', 'w')
    file_object.write('Serial_No,')
    for func in StringFunctionTables:
        for result in StringResultTable:
            file_object.write(func + ':' + result + ',')
    file_object.write('\r\n')
    file_object.close()


def calculate_result_by_input_folder(file_name, input_directory):
    file_path = []
    if os.path.isdir(input_directory):
        input_directory = os.path.abspath(input_directory)
        directory_handler = DirectoryHandler(input_directory, file_name)
        logging.info(str(directory_handler.Database_File_Path))
        file_path = directory_handler.Database_File_Path
    else:
        file_read = open(input_directory, 'r')
        for line in file_read.readlines():
            file_path.append(line)
        file_read.close()

    try:
        file_object = open(r'./query_result.csv', 'a')
        initial_table_header()
        for db_file in file_path:
            db = DatabaseHandler(db_file)
            for _data in db.Function_Status:
                file_object.write(str(_data) + ',')
        file_object.write('\r\n')
    except Exception as e:
        logging.error(str(e))
    finally:
        file_object.close()


def main():
    """
    Main program to:
    1. Call DirectoryHandler to get the list of string of all target database file
    2. for each database file, it will call DatabaseHandler to generate xml file
    :return: no return value
    """
    logging.debug(r"here is the main program")
    file_name = 'report.db'

    # if with 1 parameter
    if len(sys.argv) == 2:
        print(r"Program has 1 parameters.")
        calculate_result_by_input_folder(file_name, sys.argv[1])

    else:
        print("Use the script as below:")
        print("python(3) DbAnalyze.py [folder name] or [input file]")
        print("[folder name] shall contain a series of db which are stored")
        print("[input file] shall contain a set of directory where database files are stored")


if __name__ == '__main__':
    main()
