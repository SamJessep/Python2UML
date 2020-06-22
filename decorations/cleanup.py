from os import system

from autopep8 import fix_code

import decorator
from IO import IO


class CleanUp(decorator.Decorator):
    def __init__(self, BaseComponent, clean_source, remove_dot):
        super().__init__(BaseComponent)
        self._clean_source = clean_source
        self._remove_dot = remove_dot

    def run(self):
        if self._clean_source:
            self.clean_source_code(self.component.source_files)
        if self._remove_dot:
            for dot_file in self.component.dot_files:
                self.remove_dot_file(self.component.dot_files[dot_file])

    def clean_source_code(self, files):
        for file in files:
            IO.write(file, self.clean_code(IO.read(file)))
            print(f"cleaned file: {file}")

    @staticmethod
    def remove_dot_file(dot_path):
        system(f"del {dot_path}")

    @staticmethod
    def clean_code(code):
        return fix_code(code)
