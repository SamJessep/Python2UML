class IO:

    @staticmethod
    def write(file_name, data, encode_type="utf8"):
        with open(file_name, 'w', encoding=encode_type) as file:
            file.write(data)

    @staticmethod
    def read(file_name, encode_type="utf8"):
        with open(file_name, 'r', encoding=encode_type) as file:
            return file.read()
