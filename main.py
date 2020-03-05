import os;

import autopep8;

# will replace these with inputs when running .py file
diagram_file_name = 'UML_ClassDiagram';
diagram_file_format = 'svg';
diagram_source = 'C:\\Users\\Sam\\PycharmProjects\\Python2UML\\';

#open the python file to read the data
filename = os.environ['file'];
file = open(filename, 'r');
file_contents = file.read();
file.close();

#use AutoPep8 to clean the python code
clean_code = autopep8.fix_code(file_contents);

#add the clean code to a buffer file
bufferFile = open('buffer.py', 'w');
bufferFile.write(clean_code);
bufferFile.close();

#create .dot file, it uses first enviroment variable as input file/s
#run_pyreverse();

#pyreverse can create .dot and make UML in one command, IDK if we can keep this
#might be hard to handle errors with it
os.system(f'pyreverse {diagram_source} -o {diagram_file_format} -p {diagram_file_name}');

#below is creating UML diagram using graphviz OOP version
#src = Source('');
#src = src.from_file('classes.dot');
#src.render(format='png', filename=diagram_file_name);
