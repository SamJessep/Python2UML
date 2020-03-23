class Animal(object):
    def __init__(self, name='unknown', words='nothing'):
        print("Animal constructor")
        self.name = name
        self.words = words
        self.age = 0
        self.memories = []

    def __str__(self):
        return 'i am a(n) {} and say {}'.format(self.name, self.words)

    def speak(self):
        print(self.words)


# aAnimal = Animal()
# print(aAnimal)
# print(id(aAnimal))


class Pig(Animal):
    def __init__(self, name='piggie', words='oink'):
        print("Pig constructor")
        # Animal.__init__(self, __name, words)
        # or use super method
        # lets you avoid referring to the base class explicitly
        #
        # super().__init__(__name, words)
        # super(Pig, self).__init__(__name, words)

        # super(Bird, self) VS super() here
        super(Bird, self).__init__(name, words)


class Bird(Animal):
    def __init__(self, name='birdie', words='tweet'):
        print("Bird constructor")
        Animal.__init__(self, name, words)

    @staticmethod
    def move():
        print("flap, flap = Hey I'm flying!")


# class FluffyPig(Bird, Pig):
class FluffyPig(Pig, Bird):
    # def __init__(self, __name, words, tasteness, price):
    def __init__(self, name, words):
        print("FluffyPig constructor")
        # Animal.__init__(self, __name, words)
        super(FluffyPig, self).__init__(name, words)
        self.tasteness = 9.9
        self.price = 123.99


print(FluffyPig("FluggyPig", "OMG"))
print(FluffyPig.__mro__)


# expected output:
#
# FluffyPig constructor
# Pig constructor
# Animal constructor
# i am a(n) FluggyPig and say OMG
# (<class '__main__.FluffyPig'>, <class '__main__.Pig'>, <class '__main__.Bird'>, <class '__main__.Animal'>, <class 'object'>)


# class Clothing(object):
#     def __init__(self, name='naked'):
#         self.type = name

# class Snake(Animal):
#     def __init__(poohBah, __name='snake', words="ssss"):
#         Animal.__init__(poohBah, __name, words)
#         poohBah.pig = Pig()
#         poohBah.clothing = [Clothing('CheePoww')]
#         # print(type(poohBah))
#         # print(dir(poohBah))
#
# temp = Snake(Animal())
# print(temp)
