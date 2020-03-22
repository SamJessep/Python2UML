class class1():
    def __init__(self):
        self.parent = class2()


class class2():
    def __init__(self):
        self.child = class1()

    def do(number):
        return number


class class3(class1, class2):
    def __init__(self):
        self.parents = [class1(), class2()]
