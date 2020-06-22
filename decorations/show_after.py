from os import system

import decorator


class ShowAfter(decorator.Decorator):
    def __init__(self, BaseComponent, show_diagram, show_location):
        super().__init__(BaseComponent)
        self._show_diagram = show_diagram
        self._show_location = show_location

    def run(self):
        if self._show_diagram:
            self.show_diagram()
        if self._show_location:
            self.show_location()

    def show_diagram(self):
        cmd = f"{self.component.out_path}/{self.component.name}.{self.component.out_file_type}"
        system(cmd)

    def show_location(self):
        system(f'start {self.component.out_path}')
