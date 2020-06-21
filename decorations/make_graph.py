from re import findall

import decorator
from IO import IO
from pieChart import Pie


class MakeGraph(decorator.Decorator):
    def __init__(self, BaseComponent, files):
        super().__init__(BaseComponent)
        self.method_count = 0
        self.class_count = 0
        self.files = files

    def run(self):
        self.makeGraph()

    def makeGraph(self):
        for file in self.files:
            code = IO.read(file)
            self.method_count += len(findall('def', code))
            self.class_count += len(findall('class', code))
        pie = Pie(['methods', 'classes'], [self.method_count, self.class_count], 'Class and method relation(including '
                                                                                 'constructors)')
        pie.makePie(self.component.out_path, self.component.name)
