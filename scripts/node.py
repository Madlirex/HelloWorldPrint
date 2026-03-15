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

class IfStatement(Node):

    def __init__(self, condition, body, elifs: list[tuple] = None, else_body: list = None):
        self.condition = condition
        self.body = body
        self.elifs: list[tuple] = elifs or []
        self.else_body = else_body or []

class Return(Node):

    def __init__(self, value):
        self.value = value

class FunctionDef(Node):

    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class While(Node):

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class TryExcept(Node):

    def __init__(self, body, excepts: list[tuple] = None):
        self.body = body
        self.excepts: list[tuple] = excepts or []

class Lambda(Node):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class ForLoop(Node):

    def __init__(self, variable, expression, body):
        self.variable = variable
        self.expression = expression
        self.body = body

class ClassDef(Node):

    def __init__(self, name, body, parents = None):
        self.name = name
        self.body = body
        self.parents = parents or None

class TernaryOp(Node):

    def __init__(self, condition, value1, value2):
        self.condition = condition
        self.value1 = value1
        self.value2 = value2

class ListComprehension(Node):

    def __init__(self, variable, expression, body = None, filter_condition = None):
        self.body = body or []
        self.variable = variable
        self.expression = expression
        self.filter = filter_condition or []

class ListNode(Node):

    def __init__(self, values = None):
        self.values = values or []

class TupleNode(Node):

    def __init__(self, values = None):
        self.values = values or []

class SetNode(Node):

    def __init__(self, values = None):
        self.values = values or []

class DictionaryNode(Node):

    def __init__(self, keys = None, values = None):
        self.keys = keys or []
        self.values = values or []

class Boolean(Node):

    def __init__(self, value):
        self.value = value

class NoneNode(Node):
    pass

class Index(Node):

    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

class Slice(Node):

    def __init__(self, obj, start = None, end = None, step = None):
        self.obj = obj
        self.start = start
        self.end = end
        self.step = step

class Import(Node):

    def __init__(self, module, alias = None):
        self.module = module
        self.alias = alias

class FromImport(Node):

    def __init__(self, path, module, alias = None):
        self.path = path
        self.module = module
        self.alias = alias

class Raise(Node):

    def __init__(self, value):
        self.value = value

class Break(Node):
    pass

class Continue(Node):
    pass

class Pass(Node):
    pass

class Expression(Node):

    def __init__(self, value: str):
        self.value = value