from argparse import ArgumentParser
from glob import glob
from os import environ, pathsep
from os import system, path, getcwd

from autopep8 import fix_code
from graphviz import Source

from IO import IO

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
    parser.add_argument("SourceCodePath", help="path to input source code directory or file")
    parser.add_argument("OutputPath", help="path to save the generated diagram")

    # optional arguments with parameters
    parser.add_argument("-n", "--DiagramName", help="name for diagram when its saved, ignore extention")
    parser.add_argument("-e", "--Extension", help="set output file type"
                                                  "supported file types: png, pdf, ps, svg, svgz, fig, mif, hpgl, pcl, "
                                                  "gif, dia, imap, cmapx")

    # optional arguments without parameters
    parser.add_argument("-c", "--CleanSource", action='store_true', help="uses auto pep8 to clean the source code")
    parser.add_argument("-s", "--ShowDiagram", action='store_true', help="show the diagram after its made")
    parser.add_argument("-p", "--ShowPath", action='store_true', help="open location of the uml diagram")
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
        optional_args = {"clean_source_code": args.CleanSource, **optional_args}

    if args.CleanDOT:
        optional_args = {"clean_up_dot": args.CleanDOT, **optional_args}

    if args.ShowDiagram:
        optional_args = {"open_after": args.ShowDiagram, **optional_args}

    if args.ShowPath:
        optional_args = {"open_location_after": args.ShowPath, **optional_args}

    print(optional_args)
    p2u = Py2UML(in_path=args.SourceCodePath, out_path=args.OutputPath, **optional_args)
    p2u.create_buffer()
    p2u.make_dot('buffer.py')
    p2u.make_diagram(f'classes_{p2u.name}.dot')
    print(f"diagram has been saved to: {path.abspath(p2u.out_path)}")
