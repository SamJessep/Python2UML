# pyreverse can create .dot and make UML in one command, IDK if we can keep this
# might be hard to handle errors with it
# system(f'pyreverse [SOURCE] -o [FILETYPE] -p {FILENAME}');

# below is creating UML diagram using graphviz OOP version
# src = Source('');
# src = src.from_file('classes.dot');
# src.render(format='png', filename=diagram_file_name);
from argparse import ArgumentParser
from glob import glob;
from os import system
from shutil import move

from autopep8 import fix_code

parser = ArgumentParser()
parser.add_argument("SourceCodePath", help="path to input source code directory or file")
parser.add_argument("OutputPath", help="path to save the generated diagram")
parser.add_argument("-n", "--DiagramName", help="name for diagram when its saved, ignore extention")

outputHelp = 'set output file type e.g "-e png"' \
             "supported file types: png, pdf, ps, svg, svgz, fig, mif, hpgl, pcl, gif, dia, imap, cmapx"
parser.add_argument("-e", "--Extention", help=outputHelp)
parser.add_argument("-c", "--ClassOnly", help="creates diagram for classes only and ignores packages");
parser.add_argument("-p", "--PackageOnly", help="creates diagram for packages only and ignores classes");
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

    def read_source_code(self):
        return glob(f'{self.in_path}/**/*.py');

    def add_files_to_buffer_file(self, files):
        temp_buffer = ''
        for a_file in files:
            temp_buffer += IO.read(a_file);
        IO.write('buffer.py', self.clean_code(temp_buffer));
        return temp_buffer

    @staticmethod
    def clean_code(code):
        return fix_code(code);

    def make_diagram(self):
        # make diagram in default location then move to desired location
        print(self.in_path, self.out_path);
        system(f'pyreverse {self.in_path} -o {self.out_file_type} -p {self.name}');
        move(f'./classes_{self.name}.{self.out_file_type}', f'{self.out_path}/classes_{self.name}.{self.out_file_type}')
        move(f'./packages_{self.name}.{self.out_file_type}',
             f'{self.out_path}/packages_{self.name}.{self.out_file_type}')


print(__name__)
if __name__ == "__main__":
    optional_args = {}

    if args.DiagramName:
        optional_args += {"diagram_name": args.DiagramName}

    if args.Extention:
        optional_args += {"out_file_type": args.Extention}

    p2u = Py2UML(in_path=args.SourceCodePath, out_path=args.OutputPath, **optional_args);
    p2u.make_diagram();
