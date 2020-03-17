from argparse import ArgumentParser
from os import environ, pathsep

from py2UML import Py2UML

environ["PATH"] += pathsep + './graphviz/bin/'

parser = ArgumentParser()
parser.add_argument("SourceCodePath", help="path to input source code directory or file")
parser.add_argument("OutputPath", help="path to save the generated diagram")

# optional arguments with parameters
parser.add_argument("-n", "--DiagramName", help="name for diagram when its saved, ignore extention")
parser.add_argument("-e", "--Extention", help="set output file type"
                                              "supported file types: png, pdf, ps, svg, svgz, fig, mif, hpgl, pcl, "
                                              "gif, dia, imap, cmapx")

# optional arguments without parameters
parser.add_argument("-c", "--CleanSource", action='store_true', help="uses auto pep8 to clean the source code")
parser.add_argument("-s", "--ShowDiagram", action='store_true', help="show the diagram after its made")
parser.add_argument("-p", "--ShowPath", action='store_true', help="open location of the uml diagram")
parser.add_argument("-d", "--CleanDOT", action='store_true', help="cleans up all dot files used to generate the "
                                                                  "diagram when finished")

args = parser.parse_args()

if __name__ == "__main__":
    optional_args = {}

    if args.DiagramName:
        optional_args = {"diagram_name": args.DiagramName}

    if args.Extention:
        optional_args = {"out_file_type": args.Extention, **optional_args}

    if args.AutoPEP8:
        optional_args = {"clean_source_code": args.AutoPEP8, **optional_args}

    if args.CleanUp:
        optional_args = {"clean_up_dot": args.CleanUp, **optional_args}

    if args.Show:
        optional_args = {"open_after": args.Show, **optional_args}

    if args.FileExplorer:
        optional_args = {"open_location_after": args.FileExplorer, **optional_args}

    print(optional_args)
    p2u = Py2UML(in_path=args.SourceCodePath, out_path=args.OutputPath, **optional_args)
    p2u.create_buffer()
    print("read the code...")
    p2u.make_dot('buffer.py')
    print("made DOT file...")
    p2u.make_diagram(f'classes_{p2u.name}.dot')
    print(f"diagram has been saved to: {p2u.out_path}")
