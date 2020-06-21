from os import system

import decorator


class ShowAfter(decorator.Decorator):

    def run(self):
        pass

    def show_diagram(self):
        cmd = f"{self.component.out_path}\{self.component.name}.{self.component.out_file_type}"
        system(cmd)

    def show_location(self):
        system(f'start {self.component.out_path}')
