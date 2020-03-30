from cmd import Cmd


class CommandLine2(Cmd):
    prompt = '[Python2UML]: '
    intro = 'Python to UML class diagram command line.\nType "help" for more information.'
    
    def default(self, input):
        print('No command: %s' %input + ', try "help"')

    def do_exit(self, input):
        """Shuts down the current command line application.
        Usage: exit"""
        print('Good bye!\n')
        return True
    

test = CommandLine2()
test.cmdloop()