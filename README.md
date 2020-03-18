# Python2UML

## Command line commands

Start program
``> python [path to project]/Python2UML/``


in:
  selecting the input or source file/folder
    ``in [path to source]``
out:
  selecting the output folder
    ``out [path to output folder]``
    
filetype:
  set the output diagram file type
    ``filetype [filetype extention]
      
makeUml:
  runs the py2Uml with current settings. input and output need to set first
   ``makeUml [optional flags]``
   
## Running the module directly

``> python main.py [INPUT FOLDER/FILE] [OUTPUT FOLDER] [optionals flags]``
### optional arguments
  -h: shows help message
  -n NAME: set name for the diagram
  -e EXTENSION: set extention the for diagram
  -c: clean the source code as it reads it
  -s: open diagram after made
  -p: show diagram in explorer after made
  -d: deletes dot file when finished with it


## Features
  1. output class diagram in multiple formats(pdf, png, ...)
  2. read code from single python file
  3. read code from whole python project/directory
  4. choose export directory
  5. keep source file(.dot file/class description used to build diagram)
  6. choose whether autoPEP8 should save the cleaned version over project code(clean project code aswell)
  7. create multiple seperate diagrams in one run
  8. name diagram
  9. change orientaion of classes in diagram
  10. use exsting source file(.dot file)
  11. use alternate source file type(other file than .dot)
  
## Packages
  * graphviz - https://graphviz.readthedocs.io/en/stable/index.html
  * pylint -> pyreverse - https://pypi.org/project/pyreverse/
  * os (for running command line function from python module) - https://www.geeksforgeeks.org/python-os-system-method/
