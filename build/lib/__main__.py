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

        system(f'python py2UML.py {self.in_path} {self.out_path} -e{self.file_type} {line}')

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
