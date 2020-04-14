from os import path
from exceptions import InvalidPathError


class IO2:
    #Alternative IO for mix and matching other components together.
    @staticmethod
    def write(file_name, data, encode_type="utf8"):
        with open(file_name, 'w', encoding=encode_type) as file:
            file.write(data)

    @staticmethod
    def read(file_name, encode_type="utf8"):
        with open(file_name, 'r', encoding=encode_type) as file:
            return file.read()

    @staticmethod
    def try_path(file_path):
        path_exists = path.exists(file_path)
        if not path_exists:
            raise InvalidPathError(path=file_path)
        return path_exists
