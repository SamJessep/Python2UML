from argparse import ArgumentParser
from glob import glob
from os import system, path, getcwd, environ, pathsep
from autopep8 import fix_code
from graphviz import Source
from re import findall
from IO import IO
from pieChart import Pie

environ['PATH'] += pathsep + './graphviz/bin/'


class Py2UML:
    def __init__(self,
                 in_path='.',
                 out_path='.',
                 out_file_type='png',
                 diagram_name='class_diagram',
                 clean_source_code=False,
                 clean_up_dot=False,
                 open_after=False,
                 open_location_after=False,
                 black_list=[]
                 ):
        self.in_path = in_path
        self.out_path = out_path
        self.out_file_type = out_file_type
        self.name = diagram_name
        self.clean_source = clean_source_code
        self.clean_dot = clean_up_dot
        self.open_after = open_after
        self.open_location_after = open_location_after
        self.black_list = black_list

    def get_python_files(self):
        b_list = []
        for b in self.black_list:
            b_list += (glob(f'{self.in_path}/{b}*', recursive=True))
        b_list

        if ".py" in self.in_path:
            return [self.in_path]
        w_list = glob(f'{self.in_path}\**\*.py', recursive=True)

        new_b_list = []
        for selected_item in w_list:
            for unselected_item in b_list:
                if selected_item in unselected_item:
                    new_b_list.append(selected_item)
                    break

        return set(w_list) - set(new_b_list + b_list)

    def add_files_to_buffer_file(self, files):
        temp_buffer = ''
        for a_file in files:
            code = IO.read(a_file)
            temp_buffer += self.clean_code(code)
            if self.clean_source:
                IO.write(a_file, self.clean_code(code))
                print(f'cleaned {a_file}')
        IO.write('buffer.py', temp_buffer)
        return temp_buffer

    def create_buffer(self):
        python_files = self.get_python_files()
        # print(python_files)
        return self.add_files_to_buffer_file(python_files)

    @staticmethod
    def clean_code(code):
        return fix_code(code)

    def make_dot(self, buffer_path):
        command = f'pyreverse {buffer_path}  -p {self.name} '
        system(command)

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
        self.show_location()

    def clean_up(self, dot_path):
        if self.clean_dot:
            system(f"del {dot_path}")

    def show_location(self):
        if self.open_location_after:
            system(f'start {self.out_path}')

    def make_graph(self, buffer):
        code = IO.read(buffer)
        method_count = len(findall('def', code))
        class_count = len(findall('class', code))
        Pie(['methods', 'classes'], [method_count, class_count],
            'Class and method relation').makePie()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "SourceCodePath", help="path to input source code directory or file")
    parser.add_argument(
        "OutputPath", help="path to save the generated diagram")

    # optional arguments with parameters
    parser.add_argument("-n", "--DiagramName",
                        help="name for diagram when its saved, ignore extention")
    parser.add_argument("-b", "--BlackList",
                        help="choose folders or files to exclude")
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
    parser.add_argument("-P", "--ShowPie",
                        action='store_true', help="shows a pie chart")
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

    if args.BlackList:
        optional_args = {
            'black_list': args.BlackList.split(','), **optional_args}

    print(optional_args)
    p2u = Py2UML(in_path=args.SourceCodePath,
                 out_path=args.OutputPath, **optional_args)
    p2u.create_buffer()
    p2u.make_dot('buffer.py')
    p2u.make_diagram(f'classes_{p2u.name}.dot')

    if args.ShowPie:
        p2u.make_graph('buffer.py')

    print(f"diagram has been saved to: {path.abspath(p2u.out_path)}")
from sys import argv
from commandLine import CommandLine

if __name__ == "__main__":
    cmd = CommandLine()
    if len(argv) > 1:
        cmd.onecmd(' '.join(argv[1:]))
    else:
        cmd.cmdloop()
from cmd import Cmd
from os import system, path
from sys import argv
from exceptions import *
import pickle
from IO import IO


class CommandLine(Cmd):
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
            try:
                if IO.try_path(line):
                    self.in_path = line
                    print(f'input path set to: {line}')
            except Exception as e:
                print(e)

    def complete_in(self, line):
        print(line)

    def do_out(self, line):
        """Sets the output path
        Usage: out [PATH]"""
        if not line:
            print(f'selected output path is: {self.out_path}')
        else:
            try:
                if IO.try_path(line):
                    self.out_path = line
                    print(f'output path set to: {line}')
            except Exception as e:
                print(e)

    def do_filetype(self, line):
        """set filetype for the output diagram
        Usage: filetype [file extenstion]"""

        if not line:
            print(f'selected file type is: {self.file_type}')
        else:
            try:
                if line in self.file_types:
                    self.file_type = line
                    print(f'file type set to: {line}')
                else:
                    raise UnsupportedFileTypeError(
                        file_type=line, supported_file_types=self.file_types)
            except Exception as e:
                print(str(e))

    def complete_filetype(self, text, line, begidx, endidx):
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

    def do_saveConfig(self, savePath='.'):
        """save current configs
        Usage: saveConfig [path]"""
        public_props = (name for name in dir(self) if not name.startswith('_'))
        properties = {
            'in_path': self.in_path,
            'out_path': self.out_path,
            'file_type': self.file_type,
            'file_types': self.file_types
        }
        p = f'{savePath}cmdConfigs.p'
        print(p)
        pickle.dump(properties, open(p, 'wb'))
        print(f'configs saved to {savePath}/cmdConfigs.p')

    def do_loadConfig(self, loadPath='./cmdConfigs.p'):
        """load current configs
        Usage: loadConfig [path to config file]"""
        try:
            if not path.exists(loadPath):
                raise FileDoesntExistError(loadPath)
            if path.getsize(loadPath) > 0:
                properties = pickle.load(open(loadPath, "rb"))
                for key in properties:
                    setattr(self, key, properties[key])
                print(f"config file: {loadPath} was loaded")
            else:
                raise EmptyConfigFileError(loadPath)
        except Exception as e:
            print(str(e))

    def default(self, line):
        print('No command: %s' % line)

    def emptyline(self):
        pass

    def do_exit(self, line):
        print('exiting...')
        return True

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        system(args)

    def do_graph(self, args):
        """Unimplemented"""

    def do_database(self, args):
        """Unimplemented"""
from os import path
from exceptions import InvalidPathError


class IO:

    @staticmethod
    def write(file_name, data, encode_type="utf8"):
        with open(file_name, 'w', encoding=encode_type) as file:
            file.write(data)

    @staticmethod
    def read(file_name, encode_type="utf8"):
        with open(file_name, 'r', encoding=encode_type) as file:
            return file.read()

    @staticmethod
    def try_path(file_path):
        path_exists = path.exists(file_path)
        if not path_exists:
            raise InvalidPathError(path=file_path)
        return path_exists
import unittest

# Quick fire example unit test. Gotta add these for the main app later.


class TestMethods(unittest.TestCase):
    def test_upper(self):
        # Quick fire example doctest. Gotta integrate these into the app's commands.
        """
        >>> x = 1
        >>> x
        1
        """
        print('Testing upper')
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()
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
from distutils.core import setup
# need to update this later with dependacies needed
setup(
    # Application name:
    name="MyApplication",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="name surname",
    author_email="name@addr.ess",

    # Packages
    packages=[""],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "graphviz",
        "pylint",
        "autopep8",
        "matplotlib"
    ],
)
import matplotlib.pyplot as plt


class Pie:
    def __init__(self, labels, data, title):
        self.labels = labels
        self.data = data
        self.title = title

    def makePie(self):

        fig1, ax1 = plt.subplots()
        ax1.pie(self.data, labels=self.labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.axis('equal')
        plt.title(self.title)
        plt.show()
import sqlite3
from sqlite3 import Error


class database:
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        print('Good')
        try:
            conn = sqlite3.connect(db_file)
            print('Good')
        except Error as e:
            print(e)

        return conn


fug = database()

fug.create_connection('Test')
# Save this file for later
