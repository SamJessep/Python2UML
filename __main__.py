from cmd import Cmd
from os import system, path
from sys import argv
from exceptions import *
import pickle


def try_path(file_path):
    path_exists = path.exists(file_path)
    if not path_exists:
        raise InvalidPathError(path=file_path)
    return path_exists


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
            if try_path(line):
                self.in_path = line
                print(f'input path set to: {line}')

    def complete_in(self, line):
        print(line)

    def do_out(self, line):
        """Sets the output path
        Usage: out [PATH]"""
        if not line:
            print(f'selected output path is: {self.out_path}')
        else:
            if try_path(line):
                self.out_path = line
                print(f'output path set to: {line}')

    def do_filetype(self, line):
        """set filetype for the output diagram
        Usage: filetype [file extenstion]"""
        try:
            if not line:
                print(f'selected file type is: {self.file_type}')
            else:
                if line in self.file_types:
                    self.file_type = line
                    print(f'file type set to: {line}')
                else:
                    raise UnsupportedFileTypeError(
                        file_type=line, supported_file_types=self.file_types)
        except UnsupportedFileTypeError:
            print(UnsupportedFileTypeError.msg)

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
        if not path.exists(loadPath):
            raise FileDoesntExistError(loadPath)
        if path.getsize(loadPath) > 0:
            properties = pickle.load(open(loadPath, "rb"))
            for key in properties:
                setattr(self, key, properties[key])
            print(f"config file: {loadPath} was loaded")
        else:
            raise EmptyConfigFileError(loadPath)

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


if __name__ == "__main__":
    if len(argv) > 1:
        CLI4Py2UML().onecmd(' '.join(argv[1:]))
    else:
        CLI4Py2UML().cmdloop()
