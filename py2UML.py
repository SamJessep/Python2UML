# pyreverse can create .dot and make UML in one command, IDK if we can keep this
# might be hard to handle errors with it
# system(f'pyreverse [SOURCE] -o [FILETYPE] -p {FILENAME}');

# below is creating UML diagram using graphviz OOP version
# src = Source('');
# src = src.from_file('classes.dot');
# src.render(format='png', filename=diagram_file_name);
from argparse import ArgumentParser
from glob import glob
from os import system
from shutil import move
from graphviz import Source

from autopep8 import fix_code
import pylint

import os
os.environ["PATH"] += os.pathsep + './graphviz/bin/'

parser = ArgumentParser()
parser.add_argument("SourceCodePath", help="path to input source code directory or file")
parser.add_argument("OutputPath", help="path to save the generated diagram")
parser.add_argument("-n", "--DiagramName", help="name for diagram when its saved, ignore extention")

outputHelp = 'set output file type e.g "-e png"' \
             "supported file types: png, pdf, ps, svg, svgz, fig, mif, hpgl, pcl, gif, dia, imap, cmapx"
parser.add_argument("-e", "--Extention", help=outputHelp)
parser.add_argument("-c", "--ClassOnly", help="creates diagram for classes only and ignores packages")
parser.add_argument("-p", "--PackageOnly", help="creates diagram for packages only and ignores classes")
args = parser.parse_args()


class IO:

    @staticmethod
    def write(file_name, data):
        with open(file_name, 'w') as file:
            file.write(data)

    @staticmethod
    def read(file_name):
        with open(file_name, 'r') as file:
            return file.read()


class Py2UML:
    def __init__(self, in_path='.', out_path='.', out_file_type='png', diagram_name='class_diagram'):
        self.in_path = in_path
        self.out_path = out_path
        self.out_file_type = out_file_type
        self.name = diagram_name

    def get_python_files(self):
        if ".py" in self.in_path:
            return [self.in_path]
        return glob(f'{self.in_path}/**.py')

    def add_files_to_buffer_file(self, files):
        temp_buffer = ''
        for a_file in files:
            temp_buffer += IO.read(a_file)
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
        src.render(format=self.out_file_type, filename=self.name, directory=self.out_path)


print(__name__)
if __name__ == "__main__":
    optional_args = {}

    if args.DiagramName:
        optional_args = {"diagram_name": args.DiagramName}

    if args.Extention:
        optional_args = {"out_file_type": args.Extention, **optional_args}

    p2u = Py2UML(in_path=args.SourceCodePath, out_path=args.OutputPath, **optional_args);
    p2u.create_buffer()
    p2u.make_dot('buffer.py')
    p2u.make_diagram(f'classes_{p2u.name}.dot')
