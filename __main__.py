from sys import argv
from commandLine import CommandLine

if __name__ == "__main__":
    cmd = CommandLine()
    #Pick either
    if len(argv) > 1:
        cmd.onecmd(' '.join(argv[1:]))
    else:
        cmd.cmdloop()
