from sys import argv
from commandLine import CommandLine
from commandLine2 import CommandLine2

if __name__ == "__main__":
    cmd = CommandLine()
    #cmd = CommandLine2()
    #Pick either
    if len(argv) > 1:
        cmd.onecmd(' '.join(argv[1:]))
    else:
        cmd.cmdloop()
