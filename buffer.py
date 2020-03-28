from IO import IO
from graphviz import Source
from autopep8 import fix_code
from setup import Setup
from argparse import ArgumentParser
from glob import glob
from os import environ, pathsep
from os import system, path, getcwd
environ["PATH"] += pathsep + './graphviz/bin/'


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
        return glob(f'{self.in_path}**/*.py', recursive=True)

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
        path.abspath(getcwd())
        python_files = self.get_python_files()
        print(python_files)
        return self.add_files_to_buffer_file(python_files)

    @staticmethod
    def clean_code(code):
        return fix_code(code)

    def make_dot(self, buffer_path):
        command = f'pyreverse {buffer_path}  -p {self.name}'
        system(command)

    def make_diagram(self, dot_path):
        print(dot_path)
        src = Source(IO.read(dot_path))
        src.render(
            format=self.out_file_type,
            filename=self.name,
            directory=self.out_path,
            cleanup=self.clean_dot,
            view=self.open_after
        )
        self.clean_up(dot_path)
        self.show_location()

    def clean_up(self, dot_path):
        if self.clean_dot:
            system(f"del {dot_path}")

    def show_location(self):
        if self.open_location_after:
            system(f'start {self.out_path}')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "SourceCodePath", help="path to input source code directory or file")
    parser.add_argument(
        "OutputPath", help="path to save the generated diagram")

    # optional arguments with parameters
    parser.add_argument("-n", "--DiagramName",
                        help="name for diagram when its saved, ignore extention")
    parser.add_argument("-e", "--Extension", help="set output file type"
                                                  "supported file types: png, pdf, ps, svg, svgz, fig, mif, hpgl, pcl, "
                                                  "gif, dia, imap, cmapx")

    # optional arguments without parameters
    parser.add_argument("-c", "--CleanSource", action='store_true',
                        help="uses auto pep8 to clean the source code")
    parser.add_argument("-s", "--ShowDiagram", action='store_true',
                        help="show the diagram after its made")
    parser.add_argument("-p", "--ShowPath", action='store_true',
                        help="open location of the uml diagram")
    parser.add_argument("-d", "--CleanDOT", action='store_true', help="cleans up all dot files used to generate the "
                                                                      "diagram when finished")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    optional_args = {}

    if args.DiagramName:
        optional_args = {"diagram_name": args.DiagramName}

    if args.Extension:
        optional_args = {"out_file_type": args.Extension, **optional_args}

    if args.CleanSource:
        optional_args = {
            "clean_source_code": args.CleanSource, **optional_args}

    if args.CleanDOT:
        optional_args = {"clean_up_dot": args.CleanDOT, **optional_args}

    if args.ShowDiagram:
        optional_args = {"open_after": args.ShowDiagram, **optional_args}

    if args.ShowPath:
        optional_args = {"open_location_after": args.ShowPath, **optional_args}

    print(optional_args)
    p2u = Py2UML(in_path=args.SourceCodePath,
                 out_path=args.OutputPath, **optional_args)
    p2u.create_buffer()
    p2u.make_dot('buffer.py')
    p2u.make_diagram(f'classes_{p2u.name}.dot')
    print(f"diagram has been saved to: {path.abspath(p2u.out_path)}")
from cmd import Cmd
from os import system
from sys import argv


class CLI4Py2UML(Cmd):
    prompt = '(py2UML): '
    intro = 'python2UML CLI'

    def __init__(self):
        super().__init__(self)
        self.in_path = 'none'
        self.file_type = 'png'
        self.out_path = '.'
        self.file_types = ['png', 'pdf', 'ps', 'svg', 'svgz', 'fig', 'mif', 'hpgl', 'pcl', 'gif', 'dia', 'imap',
                           'cmapx']

    def do_in(self, line):
        """Sets the input file or directory
        Usage: in [PATH]"""
        if not line:
            print(f'selected input path is: {self.in_path}')
        else:
            self.in_path = line
            print(f'input path set to: {line}')

    def do_out(self, line):
        """Sets the output path
        Usage: out [PATH]"""
        if not line:
            print(f'selected output path is: {self.out_path}')
        else:
            self.out_path = line
            print(f'output path set to: {line}')

    def do_filetype(self, line):
        if not line:
            print(f'selected file type is: {self.file_type}')
        else:
            if line in self.file_types:
                self.file_type = line
                print(f'file type set to: {line}')
            else:
                print('invalid file type')

    def complete_filetype(self, text):
        if not text:
            completions = self.file_types[:]
        else:
            completions = [t
                           for t in self.file_types
                           if t.startswith(text)
                           ]
        return completions

    def do_makeUml(self, line):
        """Makes the class diagram using the parameters set by commands in, out, filetype
        Usage: makeUml [flags]"""

        system(
            f'python py2UML.py {self.in_path} {self.out_path} -e{self.file_type} {line}')

    def default(self, line):
        print('No command: %s' % line)

    def do_EOF(self, line):
        return True

    def do_exit(self, line):
        print('exiting...')
        return True


if __name__ == "__main__":
    if len(argv) > 1:
        CLI4Py2UML().onecmd(' '.join(argv[1:]))
    else:
        CLI4Py2UML().cmdloop()
class Animal(object):
    def __init__(self, name='unknown', words='nothing'):
        print("Animal constructor")
        self.name = name
        self.words = words
        self.age = 0
        self.memories = []

    def __str__(self):
        return 'i am a(n) {} and say {}'.format(self.name, self.words)

    def speak(self):
        print(self.words)


# aAnimal = Animal()
# print(aAnimal)
# print(id(aAnimal))


class Pig(Animal):
    def __init__(self, name='piggie', words='oink'):
        print("Pig constructor")
        # Animal.__init__(self, __name, words)
        # or use super method
        # lets you avoid referring to the base class explicitly
        #
        # super().__init__(__name, words)
        # super(Pig, self).__init__(__name, words)

        # super(Bird, self) VS super() here
        super(Bird, self).__init__(name, words)


class Bird(Animal):
    def __init__(self, name='birdie', words='tweet'):
        print("Bird constructor")
        Animal.__init__(self, name, words)

    @staticmethod
    def move():
        print("flap, flap = Hey I'm flying!")


# class FluffyPig(Bird, Pig):
class FluffyPig(Pig, Bird):
    # def __init__(self, __name, words, tasteness, price):
    def __init__(self, name, words):
        print("FluffyPig constructor")
        # Animal.__init__(self, __name, words)
        super(FluffyPig, self).__init__(name, words)
        self.tasteness = 9.9
        self.price = 123.99


print(FluffyPig("FluggyPig", "OMG"))
print(FluffyPig.__mro__)


# expected output:
#
# FluffyPig constructor
# Pig constructor
# Animal constructor
# i am a(n) FluggyPig and say OMG
# (<class '__main__.FluffyPig'>, <class '__main__.Pig'>, <class '__main__.Bird'>, <class '__main__.Animal'>, <class 'object'>)


# class Clothing(object):
#     def __init__(self, name='naked'):
#         self.type = name

# class Snake(Animal):
#     def __init__(poohBah, __name='snake', words="ssss"):
#         Animal.__init__(poohBah, __name, words)
#         poohBah.pig = Pig()
#         poohBah.clothing = [Clothing('CheePoww')]
#         # print(type(poohBah))
#         # print(dir(poohBah))
#
# temp = Snake(Animal())
# print(temp)
class Animal(object):
    def __init__(self, name='unknown', words='nothing'):
        print("Animal constructor")
        self.name = name
        self.words = words
        self.age = 0
        self.memories = []

    def __str__(self):
        return 'i am a(n) {} and say {}'.format(self.name, self.words)

    def speak(self):
        print(self.words)


# aAnimal = Animal()
# print(aAnimal)
# print(id(aAnimal))


class Pig(Animal):
    def __init__(self, name='piggie', words='oink'):
        print("Pig constructor")
        # Animal.__init__(self, __name, words)
        # or use super method
        # lets you avoid referring to the base class explicitly
        #
        # super().__init__(__name, words)
        # super(Pig, self).__init__(__name, words)

        # super(Bird, self) VS super() here
        super(Bird, self).__init__(name, words)


class Bird(Animal):
    def __init__(self, name='birdie', words='tweet'):
        print("Bird constructor")
        Animal.__init__(self, name, words)

    @staticmethod
    def move():
        print("flap, flap = Hey I'm flying!")


# class FluffyPig(Bird, Pig):
class FluffyPig(Pig, Bird):
    # def __init__(self, __name, words, tasteness, price):
    def __init__(self, name, words):
        print("FluffyPig constructor")
        # Animal.__init__(self, __name, words)
        super(FluffyPig, self).__init__(name, words)
        self.tasteness = 9.9
        self.price = 123.99


print(FluffyPig("FluggyPig", "OMG"))
print(FluffyPig.__mro__)


# expected output:
#
# FluffyPig constructor
# Pig constructor
# Animal constructor
# i am a(n) FluggyPig and say OMG
# (<class '__main__.FluffyPig'>, <class '__main__.Pig'>, <class '__main__.Bird'>, <class '__main__.Animal'>, <class 'object'>)


# class Clothing(object):
#     def __init__(self, name='naked'):
#         self.type = name

# class Snake(Animal):
#     def __init__(poohBah, __name='snake', words="ssss"):
#         Animal.__init__(poohBah, __name, words)
#         poohBah.pig = Pig()
#         poohBah.clothing = [Clothing('CheePoww')]
#         # print(type(poohBah))
#         # print(dir(poohBah))
#
# temp = Snake(Animal())
# print(temp)
class IO:

    @staticmethod
    def write(file_name, data, encode_type="utf8"):
        with open(file_name, 'w', encoding=encode_type) as file:
            file.write(data)

    @staticmethod
    def read(file_name, encode_type="utf8"):
        with open(file_name, 'r', encoding=encode_type) as file:
            return file.read()
