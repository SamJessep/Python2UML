import os

from abstract_py2UML_builder import AbstractPy2UMLBuilder
from decorations.cleanup import CleanUp
from decorations.get_files import GetFiles
from decorations.make_graph import MakeGraph
from decorations.show_after import ShowAfter


class ConcreteBuilder(AbstractPy2UMLBuilder):

    def setup(self, out_path, diagram_name, file_type):
        self.product.out_path = os.path.join(self.ROOT_DIR, out_path)
        self.product.name = diagram_name
        self.product.out_file_type = file_type

    def build_cleanup(self, clean_source, remove_dot):
        self.product.optional_features.append(CleanUp(self.product, clean_source, remove_dot))

    def build_get_files(self, in_path, black_list):
        self.product.get_files = GetFiles(self.product, os.path.join(self.ROOT_DIR, in_path), black_list)

    def build_show_after(self, show_diagram, show_path):
        self.product.optional_features.append(ShowAfter(self.product, show_diagram, show_path))

    def build_make_graph(self):
        self.product.optional_features.append(MakeGraph(self.product))
