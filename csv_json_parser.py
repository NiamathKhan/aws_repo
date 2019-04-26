import csv
import json
import os
from datetime import datetime as dt

from File_IO_Exception import File_IO_Exception

''' :type : pyboto3.s3'''


class File_Parser(object):
    def __init__(self, inputfile, outputfile):
        global __input_filepath, __output_filepath
        __input_filepath = inputfile
        __output_filepath = outputfile

    def read_as_csv(self):
        flag = False
        data = []
        try:
            if os.stat(__input_filepath).st_size != 0:
                with open(__input_filepath) as in_f:
                    reader = csv.DictReader(in_f)
                    title = reader.fieldnames
                    for row in reader:
                        data.extend([{row[i]: title[row[i]] for i in range(len(title))}])
            else:
                raise File_IO_Exception(f"input file {__input_filepath} is empty \n")
            return data
        except FileNotFoundError as e:
            raise File_IO_Exception(f"input file {__input_filepath} not found \n")
        except File_IO_Exception as e:
            print(e.message)
            return data
        except Exception as e:
            print(e)
            return data

    def write_as_json(self, data):
        flag = False
        try:
            writer = open(__output_filepath, 'a+')
            writer.write(json.dumps(data))
            writer.close()
            is_file_created = os.path.isfile(__output_filepath)
            if is_file_created:
                format = '%y-%m-%d %H:%M:%S'
                c_d_t = dt.now().strftime(format)
                c_stamp = dt.strptime(c_d_t, format)
                m_d_t = dt.fromtimestamp(os.path.getmtime(__output_filepath)).strftime(format)
                m_stamp = dt.strptime(m_d_t, format)
                if c_stamp >= m_stamp:
                    flag = True
            return flag
        except FileNotFoundError as e:
            raise File_IO_Exception(f"output file {__output_filepath} not found !")
        except File_IO_Exception as e:
            print(e.message)
            return flag
        except Exception as e:
            print(e)
            return flag
