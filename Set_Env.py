import boto3
import os


class Props_Exception(Exception):
    def __init__(self, message):
        self.message = message


class Set_Env(object):
    def __init__(self):
        self.session = None
        try:
            self.__properties_file = os.environ['properties_path']
            if os.stat(self.__properties_file).st_size != 0:
                with open(self.__properties_file) as p_f:
                    for line in p_f.readlines():
                        k_v = line.strip("\n").split("=")
                        os.environ[k_v[0]] = k_v[1]
                self.session = boto3.Session()
            else:
                raise Props_Exception(f"config properties file {self.__properties_file} is empty has not content !")
        except Props_Exception as e:
            print(e.message)
        except Exception as e:
            print(e)
