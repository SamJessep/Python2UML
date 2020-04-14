from cmd import Cmd
from IO2 import IO2


class CommandLine2(Cmd):
    #Alternative CommandLine for mix and matching other components together.
    prompt = '[Python2UML]: '
    intro = 'Python to UML class diagram command line.\nType "help" for more information.'
    input_path = '.'
    output_path = '.testArea/output' #default path if none is set
    
    def default(self, input):
        print('No command: "%s"' %input + ', try "help"')

    def do_exit(self, input):
        """Shuts down the current command line application.
        Usage: exit"""
        print('Good bye!\n')
        return True
    
    def do_input(self, line):
        """Sets the input file or directory.
        Defaults to current directory.
        Usage: in [PATH]"""
        try:
            if line:
                try:
                    if IO2.try_path(line):
                        self.input_path = line
                    else:
                        #This else statement will never be called unless I rework the IO
                        print('PRESS F')
                        return
                except Exception as e:
                    print(e)
            print(f'selected input path is: {self.input_path}')
        except Exception as e:
                print(e)
    
    def do_output(self, line):
        """Sets the path to output diagrams to.
        Defaults to output folder.
        Usage: out [PATH]"""
        try:
            if line:
                try:
                    if IO2.try_path(line):
                        self.output_path = line
                    else:
                        #This else statement will never be called unless I rework the IO
                        print('PRESS F')
                        return
                except Exception as e:
                    print(e)
            print(f'selected input path is: {self.output_path}')
        except Exception as e:
                print(e)
    
    def do_saveConfig(self, savePath='.'):
        """save current configs
        Usage: saveConfig [path]"""
        
        '''Write this but better
        
        try:
            if not path.exists(savePath):
                raise FileDoesntExistError(savePath)
        except Exception as e:
            print(str(e))
            return
        public_props = (name for name in dir(self) if not name.startswith('_'))
        properties = {
            'in_path': self.in_path,
            'out_path': self.out_path,
            'file_type': self.file_type,
            'file_types': self.file_types
        }
        p = f'{savePath}./cmdConfigs.p'
        print(p)
        pickle.dump(properties, open(p, 'wb'))
        print(f'configs saved to {savePath}/cmdConfigs.p')
        '''

    def do_loadConfig(self, loadPath='./cmdConfigs.p'):
        """load current configs
        Usage: loadConfig [path to config file]"""

        '''Write this but better
        try:
            if not path.exists(loadPath):
                raise FileDoesntExistError(loadPath)
            if path.getsize(loadPath) > 0:
                properties = pickle.load(open(loadPath, "rb"))
                for key in properties:
                    setattr(self, key, properties[key])
                print(f"config file: {loadPath} was loaded")
            else:
                raise EmptyConfigFileError(loadPath)
        except Exception as e:
            print(str(e))
        '''