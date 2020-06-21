import abc


class Component(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self):
        pass
