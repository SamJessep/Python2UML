from os import system

from autopep8 import fix_code

import decorator
from IO import IO


class CleanUp(decorator.Decorator):
    def __init__(self, BaseComponent):
        super().__init__(BaseComponent)

    def run(self):
        pass

    def clean_source_code(self, files):
        for file in files:
            IO.write(file, self.clean_code(IO.read(file)))
            print(f"cleaned file: {file}")

    @staticmethod
    def remove_dot_files(dot_path):
        system(f"del {dot_path}")

    @staticmethod
    def clean_code(code):
        return fix_code(code)
