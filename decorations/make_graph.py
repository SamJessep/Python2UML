from re import findall

import decorator
from IO import IO
from pieChart import Pie


class MakeGraph(decorator.Decorator):
    def __init__(self, BaseComponent):
        super().__init__(BaseComponent)
        self.method_count = 0
        self.class_count = 0

    def run(self):
        self.makeGraph(self.component.source_files)

    def makeGraph(self, files):
        for file in files:
            code = IO.read(file)
            self.method_count += len(findall('def', code))
            self.class_count += len(findall('class', code))
        pie = Pie(['methods', 'classes'], [self.method_count, self.class_count], 'Class and method relation(including '
                                                                                 'constructors)')
        pie.make_pie(self.component.out_path, self.component.name)
