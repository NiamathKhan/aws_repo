class File_IO_Exception(Exception):
    def __init__(self, message):
        self.message = message


class S3_Exception(File_IO_Exception):
    def __init__(self, message):
        self.message = message
