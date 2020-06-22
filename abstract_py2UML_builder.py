import abc
import os

import diagramMaker


class AbstractPy2UMLBuilder(metaclass=abc.ABCMeta):

    def __init__(self):
        self.product = diagramMaker.DiagramMaker()
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    @abc.abstractmethod
    def setup(self, out_path, diagram_name, file_type):
        pass

    @abc.abstractmethod
    def build_cleanup(self, clean_source, remove_dot):
        pass

    @abc.abstractmethod
    def build_get_files(self, in_path, black_list):
        pass

    @abc.abstractmethod
    def build_show_after(self, show_diagram, show_path):
        pass

    @abc.abstractmethod
    def build_make_graph(self):
        pass
