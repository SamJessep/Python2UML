from glob import glob
from os import system

from autopep8 import fix_code
from graphviz import Source

from IO import IO


class Py2UML:
    def __init__(self,
                 in_path='.',
                 out_path='.',
                 out_file_type='png',
                 diagram_name='class_diagram',
                 clean_source_code=False,
                 clean_up_dot=False,
                 open_after=False,
                 open_location_after=False
                 ):
        self.in_path = in_path
        self.out_path = out_path
        self.out_file_type = out_file_type
        self.name = diagram_name
        self.clean_source = clean_source_code
        self.clean_dot = clean_up_dot
        self.open_after = open_after
        self.open_location_after = open_location_after

    def get_python_files(self):
        if ".py" in self.in_path:
            return [self.in_path]
        return glob(f'{self.in_path}/**.py')

    def add_files_to_buffer_file(self, files):
        temp_buffer = ''
        for a_file in files:
            code = IO.read(a_file)
            temp_buffer += code
            if self.clean_source:
                IO.write(a_file, self.clean_code(code))
        IO.write('buffer.py', self.clean_code(temp_buffer))
        return temp_buffer

    def create_buffer(self):
        python_files = self.get_python_files()
        print(python_files)
        return self.add_files_to_buffer_file(python_files)

    @staticmethod
    def clean_code(code):
        return fix_code(code)

    def make_dot(self, buffer_path):
        system(f'pyreverse {buffer_path}  -p {self.name}')

    def make_diagram(self, dot_path):
        src = Source(IO.read(dot_path))
        src.render(
            format=self.out_file_type,
            filename=self.name,
            directory=self.out_path,
            cleanup=self.clean_dot,
            view=self.open_after
        )
        self.clean_up(dot_path)
        self.show_location(f"{self.out_path}/{self.name}.{self.out_file_type}")

    def clean_up(self, path):
        if self.clean_dot:
            system(f"del {path}")

    def show_location(self, diagram_location):
        if self.open_location_after:
            diagram_location = diagram_location.replace('/', '\\')
            system(f'explorer /select,"{diagram_location}"')
