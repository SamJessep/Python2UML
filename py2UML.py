from argparse import ArgumentParser
from argparse import ArgumentParser
from glob import glob
from os import system, path, environ, pathsep
from re import findall

from autopep8 import fix_code
from graphviz import Source

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

    def select_files(self):
        black_list = []
        for b in self.black_list:
            black_list += (glob(f'{self.in_path}/{b}*', recursive=True))
        if ".py" in self.in_path:
            return [self.in_path]
        w_list = glob(f'{self.in_path}\**\*.py', recursive=True)

        for selected_item in w_list:
            for unselected_item in black_list:
                if selected_item in unselected_item:
                    black_list.append(selected_item)
                    break

        return set(w_list) - set(black_list)

    def get_files(self):
        python_files = self.select_files()
        if self.clean_source:
            for file in python_files:
                IO.write(file, self.clean_code(IO.read(file)))
                print(f"cleaned file: {file}")
        print(python_files)
        return " ".join(python_files)

    @staticmethod
    def clean_code(code):
        return fix_code(code)

    def make_dot(self, files):
        command = f'pyreverse {files}  -p {self.name}'
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
        self.clean_up(f"packages_{self.name}.dot")
        self.show_location()

    def clean_up(self, dot_path):
        if self.clean_dot:
            system(f"del {dot_path}")

    def show_location(self):
        if self.open_location_after:
            system(f'start {self.out_path}')

    def make_graph(self, buffer):
        code = IO.read(buffer);
        method_count = len(findall('def', code))
        class_count = len(findall('class', code))
        Pie(['methods', 'classes'], [method_count, class_count], 'Class and method relation').makePie()

    @staticmethod
    def run(in_path, out_path, DiagramName=None, file_type=None, black_list=None, clean_source=False, remove_dots=False,
            make_pie=False, show_diagram=False,
            show_path=False):
        optional_args = {}

        if DiagramName:
            optional_args = {"diagram_name": DiagramName}

        if file_type:
            optional_args = {"out_file_type": file_type, **optional_args}

        if clean_source:
            optional_args = {"clean_source_code": clean_source, **optional_args}

        if remove_dots:
            optional_args = {"clean_up_dot": remove_dots, **optional_args}

        if show_diagram:
            optional_args = {"open_after": show_diagram, **optional_args}

        if show_path:
            optional_args = {"open_location_after": show_path, **optional_args}

        if black_list:
            optional_args = {'black_list': black_list, **optional_args}

        print(optional_args)
        p2u = Py2UML(in_path=in_path, out_path=out_path, **optional_args)
        files = p2u.get_files()
        p2u.make_dot(files)
        p2u.make_diagram(f'classes_{p2u.name}.dot')

        if make_pie:
            p2u.make_graph('buffer.py')

        print(f"diagram has been saved to: {path.abspath(p2u.out_path)}")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("SourceCodePath", help="path to input source code directory or file")
    parser.add_argument("OutputPath", help="path to save the generated diagram")

    # optional arguments with parameters
    parser.add_argument("-n", "--DiagramName", help="name for diagram when its saved, ignore extention")
    parser.add_argument("-b", "--BlackList", help="choose folders or files to exclude")
    parser.add_argument("-e", "--Extension", help="set output file type"
                                                  "supported file types: png, pdf, ps, svg, svgz, fig, mif, hpgl, pcl, "
                                                  "gif, dia, imap, cmapx")

    # optional arguments without parameters
    parser.add_argument("-c", "--CleanSource", action='store_true', help="uses auto pep8 to clean the source code")
    parser.add_argument("-s", "--ShowDiagram", action='store_true', help="show the diagram after its made")
    parser.add_argument("-p", "--ShowPath", action='store_true', help="open location of the uml diagram")
    parser.add_argument("-P", "--ShowPie", action='store_true', help="shows a pie chart")
    parser.add_argument("-d", "--CleanDOT", action='store_true', help="cleans up all dot files used to generate the "
                                                                      "diagram when finished")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    Py2UML.run(args.SourceCodePath,
               args.OutputPath,
               args.DiagramName,
               args.Extension,
               args.BlackList.split(','),
               args.CleanSource,
               args.CleanDOT,
               args.ShowPie,
               args.ShowDiagram,
               args.ShowPath)
