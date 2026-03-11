class Node:
    pass


class Variable(Node):

    def __init__(self, name):
        self.name = name


class Number(Node):

    def __init__(self, value):
        self.value = value


class String(Node):

    def __init__(self, value):
        self.value = value


class Attribute(Node):

    def __init__(self, obj, name):
        self.obj = obj
        self.name = name


class Call(Node):

    def __init__(self, func, args):
        self.func = func
        self.args = args


class Assignment(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right

class Program(Node):

    def __init__(self):
        self.nodes = []