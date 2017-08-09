# -*- coding:utf-8 -*-
import logging
import os
import sqlite3

from EnumFunctionTable import StringFunctionTables, StringResultTable


class DatabaseHandler:
    """
    The class is to deal with sqlite3 database file.
    It will do the job as below:
    1. read the database
    2. Find the target service function
    3. Analyze if the target service function has a <content> which stores the xml file of the function result data
    4. If <content> is found, extract the content.
    5. convert the <content> with base64 decode and save to a xml file
    """
    Database_Name = 'report.db'
    System_SerialNo = ""
    Function_Status = []

    def __init__(self, file_name, output_path=r'./'):
        """
        :param file_name: database file name for analyze
        :param output_path: the path of output xml files. default as ./
        """
        # deal with input database file
        if os.path.isfile(file_name):
            self.Database_Name = file_name
        else:
            logging.error(r'Can not find input file.')
            return
        # connect to database
        try:
            self.Connection = sqlite3.connect(self.Database_Name)
            logging.debug(r'Database connected')
            # set the 1st data as system serial number
            self.Function_Status.append(self.get_serial_number())
            # after get serial number, create/check the output path
            # iterate the function tables to extract xml file
            for str_functions in StringFunctionTables:
                for str_result in StringResultTable:
                    self.Function_Status.append(self.read_data(str_functions, str_result))
        except Exception as e:
            logging.error(str(e))
        finally:
            self.Connection.close()

    def read_data(self, function_type, function_result):
        """
        read the data of target service function from database.
        if the target service function has been found, it will call parse_xml function.
        :param function_result: target service function result. Should be stored in EnumFunctionTable.py
        :param function_type: target service function name. Should be stored in EnumFunctionTable.py
        :return: return how many records found
        """
        if function_type not in StringFunctionTables:
            logging.error(r'Function Type is not in EnumFunctionTable.py. Please configure it first or check spelling')
            return
        logging.debug(function_type + r" is now under query.")
        sql_cursor = self.Connection.cursor()
        sql_string = r"select count(starttime) from functionstable where (functionstatus=? and FunctionType=?) "
        try:
            sql_cursor.execute(sql_string, [function_result, function_type])
            result = sql_cursor.fetchone()
            if result is None:
                logging.debug(function_type + r' with ' + function_result + ' result has not been found.!!!!!!!!!!')
                return
            else:
                logging.info(r'Read data successfully.')
                return result[0]
        except sqlite3.Error as e:
            logging.error(str(e))
        finally:
            sql_cursor.close()

    def get_serial_number(self):
        """
        this function is to fill the class variable "system_serial_no"
        The system serial no will be used as the output folder name
        :return: no return value
        """
        logging.debug(r"It is now query for system serial number.")
        sql_cursor = self.Connection.cursor()
        sql_string = r"select data from servicereportstable order by starttime desc limit 1"
        try:
            sql_cursor.execute(sql_string)
            result = sql_cursor.fetchone()
            if result is None:
                logging.warning(r"Can not find serial number!")
                return
            find_string = r'System SerialNumber="'
            find_index = str(result).find(find_string)
            system_serial_no = str(result)[find_index+len(find_string):find_index+len(find_string)+6]
            logging.info(system_serial_no)
            return system_serial_no
        except sqlite3.Error as e:
            logging.error(str(e))
        finally:
            sql_cursor.close()


if __name__ == '__main__':
    print("please do not use it individually.")
    # belows codes for debug
    # define the logging config, output in file
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=r'./DatabaseHandler.log',
                        filemode='w')
    # define a stream that will show log level > Warning on screen also
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    a = DatabaseHandler(r"./data/report.db")
    print(a.Function_Status)
