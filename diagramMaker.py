from os import system, path, environ, pathsep

from graphviz import Source

from IO import IO
from component import Component

environ['PATH'] += pathsep + './graphviz/bin/'


class DiagramMaker(Component):
    def __init__(self,
                 out_path='.',
                 out_file_type='png',
                 diagram_name='unnamed_diagram',
                 ):
        self.out_path = out_path
        self.out_file_type = out_file_type
        self.name = diagram_name

        self.source_files = []
        self.dot_files = {}
        self.get_files = None
        self.optional_features = []

    def make_dot(self, source_files):
        command = f'py -3 -mpy_reverse {" ".join(source_files)}  -p{self.name}'
        system(command)
        dots = {"class": f"classes_{self.name}.dot"}
        if path.exists(f"packages_{self.name}.dot"):
            dots['package'] = f"packages_{self.name}.dot"
        self.dot_files = dots
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
