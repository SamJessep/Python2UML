class IO:

    @staticmethod
    def write(file_name, data):
        with open(file_name, 'w') as file:
            file.write(data)

    @staticmethod
    def read(file_name):
        with open(file_name, 'r') as file:
            return file.read()
