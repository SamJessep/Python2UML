import abc

import component


class Decorator(component.Component):
    def __init__(self, BaseComponent):
        self.component = BaseComponent

    @abc.abstractmethod
    def run(self):
        self.component.run()
