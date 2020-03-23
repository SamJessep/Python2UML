class Error(Exception):
    pass


class InvalidPathError(Error):
    """Raised when selected path doesnt exist"""

    def __str__(self):
        return self.value

    def __init__(self, path):
        self.value = f'path: "{path}" is invalid, check the path entered exists'


class UnsupportedFileTypeError(Error):
    """Raised when selected file type isnt supported"""

    def __str__(self):
        return self.value

    def __init__(self, file_type, supported_file_types):
        self.value = f'"{file_type}" is an unsupported filetype \n' \
                     f'try using one of the following filetypes: {", ".join(supported_file_types)} '
        self.msg = self.value


class FileDoesntExistError(Error):
    """Selected file doesnt exist"""

    def __str__(self):
        return self.value

    def __init__(self, file_path):
        self.value = f'"{file_path}" file doesnt exist check the file path is correct'


class EmptyConfigFileError(Error):
    """Raised when selected config file is empty"""

    def __str__(self):
        return self.value

    def __init__(self, file_path):
        self.value = f'"the config file :{file_path}" is empty'
