class Node:
    pass


class Variable(Node):

    def __init__(self, name: str) -> None:
        self.name: str = name


class Number(Node):

    def __init__(self, value: int) -> None:
        self.value: int = value


class String(Node):

    def __init__(self, value: str) -> None:
        self.value: str = value


class Attribute(Node):

    def __init__(self, obj: Node, name: str) -> None:
        self.obj: Node = obj
        self.name: str = name


class Call(Node):

    def __init__(self, func: Node, args: list[Node]) -> None:
        self.func: Node = func
        self.args: list[Node] = args


class Assignment(Node):

    def __init__(self, left: list[Node], right: list[Node], operator: str = "=") -> None:
        self.left: list[Node] = left
        self.right: list[Node] = right
        self.operator: str = operator

class Program(Node):

    def __init__(self) -> None:
        self.nodes: list[Node] = []

class IfStatement(Node):

    def __init__(self, condition: Node, body: list[Node], elifs: list[tuple[Node, list[Node]]] = None, else_body: list[Node] = None) -> None:
        self.condition: Node = condition
        self.body: list[Node] = body
        self.elifs: list[tuple[Node, list[Node]]] = elifs or []
        self.else_body: list[Node] = else_body or []

class Return(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

class FunctionDef(Node):

    def __init__(self, name: str, params: list[str], body: list[Node]) -> None:
        self.name: str = name
        self.params: list[str] = params
        self.body: list[Node] = body

class While(Node):

    def __init__(self, condition: Node, body: list[Node]) -> None:
        self.condition: Node = condition
        self.body: list[Node] = body

class TryExcept(Node):

    def __init__(self, body: list[Node], excepts: list[tuple[Node, list[Node]]] = None) -> None:
        self.body: list[Node] = body
        self.excepts: list[tuple[Node, list[Node]]] = excepts or []

class Lambda(Node):
    def __init__(self, params: list[Variable], body: Node) -> None:
        self.params: list[Variable] = params
        self.body: Node = body

class ForLoop(Node):

    def __init__(self, variable: list[Variable], expression: Node, body: list[Node], else_body: list[Node] = None) -> None:
        self.variable: list[Variable] = variable
        self.expression: Node = expression
        self.body: list[Node] = body
        self.else_body = else_body or []

class ClassDef(Node):

    def __init__(self, name: str, body: list[Node], parents: list[Node] = None) -> None:
        self.name: str = name
        self.body: list[Node] = body
        self.parents: list[Node] = parents or []

class TernaryOp(Node):

    def __init__(self, condition: Node, value1: Node, value2: Node) -> None:
        self.condition: Node = condition
        self.value1: Node = value1
        self.value2: Node = value2

class ListComprehension(Node):

    def __init__(self, variable: list[Variable], expression: Node, body: list[Node] = None, filter_condition: Node | None = None) -> None:
        self.body: list[Node] = body or []
        self.variable: list[Variable] = variable
        self.expression: Node = expression
        self.filter: Node | None = filter_condition

class ListNode(Node):

    def __init__(self, values: list[Node] = None) -> None:
        self.values: list[Node] = values or []

class TupleNode(Node):

    def __init__(self, values: list[Node] = None) -> None:
        self.values: list[Node] = values or []

class SetNode(Node):

    def __init__(self, values: list[Node] = None) -> None:
        self.values: list[Node] = values or []

class DictionaryNode(Node):

    def __init__(self, keys: list[Node] = None, values: list[Node] = None) -> None:
        self.keys: list[Node] = keys or []
        self.values: list[Node] = values or []

class Boolean(Node):

    def __init__(self, value: bool) -> None:
        self.value: bool = value

class NoneNode(Node):
    pass

class Index(Node):

    def __init__(self, obj: Node, index: Node) -> None:
        self.obj: Node = obj
        self.index: Node = index

class Slice(Node):

    def __init__(self, obj: Node, start: Node | None = None, end: Node | None = None, step: Node | None = None) -> None:
        self.obj: Node = obj
        self.start: Node | None = start
        self.end: Node | None = end
        self.step: Node | None = step

class Import(Node):

    def __init__(self, module: list[Variable], alias: list[Variable]= None) -> None:
        self.module: list[Variable] = module
        self.alias: list[Variable] = alias or []

class FromImport(Node):

    def __init__(self, path: Variable, module: list[Variable], alias: list[Variable] = None) -> None:
        self.path: Variable = path
        self.module: list[Variable] = module
        self.alias: list[Variable] = alias or []

class Raise(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

class Break(Node):
    pass

class Continue(Node):
    pass

class Pass(Node):
    pass

class Expression(Node):

    def __init__(self, value: str) -> None:
        self.value: str = value

class Yield(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

class MatchNode(Node):

    def __init__(self, variable: Node, values: list[tuple[Node, list[Node]]]) -> None:
        self.variable: Node = variable
        self.values: list[tuple[Node, list[Node]]] = values

class AndNode(Node):

    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node =  left
        self.right: Node = right

class OrNode(Node):

    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node = left
        self.right: Node = right

class NotNode(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

class Operation(Node):

    def __init__(self, left: Node, right: Node, operator: str) -> None:
        self.left: Node = left
        self.right: Node = right
        self.operator: str = operator

class InNode(Node):

    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node = left
        self.right: Node = right

class IsNode(Node):

    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node = left
        self.right: Node = right
