from argparse import ArgumentParser
from os import system, path, environ, pathsep

from graphviz import Source

from IO import IO
from component import Component
from decorations.cleanup import CleanUp
from decorations.get_files import GetFiles
from decorations.make_graph import MakeGraph
from decorations.show_after import ShowAfter

environ['PATH'] += pathsep + './graphviz/bin/'


class Py2UML(Component):
    def __init__(self,
                 out_path='.',
                 out_file_type='png',
                 diagram_name='class_diagram',
                 ):
        self.out_path = out_path
        self.out_file_type = out_file_type
        self.name = diagram_name

    def make_dot(self, source_files):
        command = f'pyreverse {" ".join(source_files)}  -p {self.name}'
        system(command)
        dots = {"class": f"classes_{self.name}.dot"}
        if path.exists(f"packages_{self.name}.dot"):
            dots['package'] = f"packages_{self.name}.dot"
        return dots

    def make_diagram(self, dot_file_path):
        src = Source(IO.read(dot_file_path))
        src.render(
            format=self.out_file_type,
            filename=self.name,
            directory=self.out_path,
            cleanup=True
        )
        return f"{self.out_path}/{self.name}.{self.out_file_type}"

    def run(self):  # pragma: no cover
        self.start(".", self.out_path, self.name, self.out_file_type)

    @staticmethod
    def start(in_path, out_path, diagram_name=None, file_type=None, black_list=None, clean_source=False,
              remove_dots=False, make_pie=False, show_diagram=False,
              show_path=False):
        p2uml = Py2UML(out_path, file_type, diagram_name)
        clean = CleanUp(p2uml)
        show = ShowAfter(p2uml)
        files = GetFiles(p2uml, in_path, black_list).run()
        # make dot
        dot_paths = p2uml.make_dot(files)
        # generate diagram
        p2uml.make_diagram(dot_paths["class"])
        if clean_source:
            clean.clean_source_code(files)
        if remove_dots:
            for dot_path in dot_paths:
                clean.remove_dot_file(dot_paths[dot_path])
        if show_diagram:  # pragma: no cover
            show.show_diagram()
        if show_path:  # pragma: no cover
            show.show_location()
        if make_pie:
            graph = MakeGraph(p2uml, files)
            graph.run()


def parse_args():  # pragma: no cover
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


if __name__ == "__main__":  # pragma: no cover
    args = parse_args()
    Py2UML.start(args.SourceCodePath,
                 args.OutputPath,
                 args.DiagramName,
                 args.Extension,
                 args.BlackList.split(','),
                 args.CleanSource,
                 args.CleanDOT,
                 args.ShowPie,
                 args.ShowDiagram,
                 args.ShowPath)
