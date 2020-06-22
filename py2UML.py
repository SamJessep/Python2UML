from argparse import ArgumentParser
from os import environ, pathsep

from director import Director
from py2UML_builder import ConcreteBuilder

environ['PATH'] += pathsep + './graphviz/bin/'


class Py2UML:

    @staticmethod
    def start(in_path, out_path, diagram_name="no_name", file_type="png", black_list=None, clean_source=False,
              remove_dots=False, make_pie=False, show_diagram=False,
              show_path=False):
        features = {
            "in_path": in_path,
            "out_path": out_path,
            "file_type": file_type,
            "diagram_name": diagram_name,
            "black_list": black_list,
            "clean_source": clean_source,
            "remove_dots": remove_dots,
            "make_pie": make_pie,
            "show_diagram": show_diagram,
            "show_path": show_path
        }
        Py2UML.run(features)

    @staticmethod
    def run(features):
        concrete_builder = ConcreteBuilder()
        director = Director()
        director.set_features(features)

        director.construct(concrete_builder)
        product = concrete_builder.product
        #  mandatory
        product.get_files.run()
        product.make_dot(product.source_files)
        product.make_diagram(product.dot_files["class"])
        print(f"diagram saved to: {product.out_path}\\{product.name}.{product.out_file_type}")
        #  optionals
        for feature in product.optional_features:
            feature.run()


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
    Py2UML.start(in_path='.' if args.SourceCodePath is None else args.SourceCodePath,
                 out_path='.' if args.OutputPath is None else args.OutputPath,
                 diagram_name="unnamed_diagram" if args.DiagramName is None else args.DiagramName,
                 file_type='png' if args.Extension is None else args.Extension,
                 black_list=None if args.BlackList is None else args.BlackList.split(","),
                 clean_source=False if args.CleanSource is None else args.CleanSource,
                 remove_dots=False if args.CleanDOT is None else args.CleanDOT,
                 make_pie=False if args.ShowPie is None else args.ShowPie,
                 show_diagram=False if args.ShowDiagram is None else args.ShowDiagram,
                 show_path=False if args.ShowPath is None else args.ShowPath)
