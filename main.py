
# pyreverse can create .dot and make UML in one command, IDK if we can keep this
# might be hard to handle errors with it
# system(f'pyreverse [SOURCE] -o [FILETYPE] -p {FILENAME}');

# below is creating UML diagram using graphviz OOP version
# src = Source('');
# src = src.from_file('classes.dot');
# src.render(format='png', filename=diagram_file_name);

from glob import glob;
from os import system
from shutil import move
from sys import argv

from autopep8 import fix_code


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


# location = ".\\testArea\\projects\\mypy-master\\mypyc"
location = argv[1]

# output = ".\\testArea\\output"
output = argv[2]

# name = "myPy_ClassDiagram";
name = argv[3]

# probably gonna use some flags for some option params such as changing filetype for output
out_file_type = 'svg';

print(name, location, output)
p2u = Py2UML(diagram_name=name, in_path=location, out_file_type=out_file_type, out_path=output);
p2u.make_diagram();