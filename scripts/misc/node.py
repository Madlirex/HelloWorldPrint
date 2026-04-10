class Node:

    def accept(self, visitor):
        raise NotImplementedError

class Block(Node):

    def __init__(self, nodes: list[Node] = None) -> None:
        self.nodes: list[Node] = nodes or []

    def accept(self, visitor):
        visitor.visit_assignment(self)

class Variable(Node):

    def __init__(self, name: str) -> None:
        self.name: str = name

    def accept(self, visitor):
        return visitor.visit_variable(self)

class Number(Node):

    def __init__(self, value: int | float) -> None:
        self.value: int | float = value

    def accept(self, visitor):
        return visitor.visit_number(self)

class String(Node):

    def __init__(self, value: str) -> None:
        self.value: str = value

    def accept(self, visitor):
        return visitor.visit_string(self)

class Attribute(Node):

    def __init__(self, obj: Node, name: str) -> None:
        self.obj: Node = obj
        self.name: str = name

    def accept(self, visitor):
        return visitor.visit_attribute(self)

class Call(Node):

    def __init__(self, func: Node, args: list[Node]) -> None:
        self.func: Node = func
        self.args: list[Node] = args

    def accept(self, visitor):
        return visitor.visit_call(self)

class Assignment(Node):

    def __init__(self, left: list[Node], right: list[Node], operator: str = "=") -> None:
        self.left: list[Node] = left
        self.right: list[Node] = right
        self.operator: str = operator

    def accept(self, visitor):
        return visitor.visit_assignment(self)

class IfStatement(Node):

    def __init__(self, condition: Node, body: Block, elifs: list[tuple[Node, Block]] = None, else_body: Block = None) -> None:
        self.condition: Node = condition
        self.body: Block = body
        self.elifs: list[tuple[Node, Block]] = elifs or []
        self.else_body: Block = else_body or Block([Pass()])

    def accept(self, visitor):
        return visitor.visit_if(self)

class Return(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

    def accept(self, visitor):
        return visitor.visit_return(self)

class FunctionDef(Node):

    def __init__(self, name: str, body: Block, params: list[Node] = None) -> None:
        self.name: str = name
        self.params: list[Node] = params or []
        self.body: Block = body

    def accept(self, visitor):
        return visitor.visit_function(self)

class While(Node):

    def __init__(self, condition: Node, body: Block) -> None:
        self.condition: Node = condition
        self.body: Block = body

    def accept(self, visitor):
        return visitor.visit_while(self)

class TryExcept(Node):

    def __init__(self, body: Block, excepts: list[tuple[Node, Block]] = None) -> None:
        self.body: Block = body
        self.excepts: list[tuple[Node, Block]] = excepts or []

    def accept(self, visitor):
        return visitor.visit_try(self)

class Lambda(Node):
    def __init__(self, params: list[Variable], body: Node) -> None:
        self.params: list[Variable] = params
        self.body: Node = body

    def accept(self, visitor):
        return visitor.visit_lambda(self)

class ForLoop(Node):

    def __init__(self, variable: list[Node], expression: Node, body: Block, else_body: Block = None) -> None:
        self.variable: list[Node] = variable
        self.expression: Node = expression
        self.body: Block = body
        self.else_body: Block = else_body or Block([Pass()])

    def accept(self, visitor):
        return visitor.visit_for(self)

class ClassDef(Node):

    def __init__(self, name: str, body: Block, parents: list[Node] = None) -> None:
        self.name: str = name
        self.body: Block = body
        self.parents: list[Node] = parents or []

    def accept(self, visitor):
        return visitor.visit_class(self)


class TernaryOp(Node):

    def __init__(self, condition: Node, value1: Node, value2: Node) -> None:
        self.condition: Node = condition
        self.value1: Node = value1
        self.value2: Node = value2

    def accept(self, visitor):
        return visitor.visit_ternary(self)

class ListComprehension(Node):

    def __init__(self, variable: list[Variable], expression: Node, body: list[Node] = None, filter_condition: Node | None = None) -> None:
        self.body: list[Node] = body or []
        self.variable: list[Variable] = variable
        self.expression: Node = expression
        self.filter: Node | None = filter_condition

    def accept(self, visitor):
        return visitor.visit_list_comp(self)

class ListNode(Node):

    def __init__(self, values: list[Node] = None) -> None:
        self.values: list[Node] = values or []

    def accept(self, visitor):
        return visitor.visit_list(self)

class TupleNode(Node):

    def __init__(self, values: list[Node] = None) -> None:
        self.values: list[Node] = values or []

    def accept(self, visitor):
        return visitor.visit_tuple(self)

class SetNode(Node):

    def __init__(self, values: list[Node] = None) -> None:
        self.values: list[Node] = values or []

    def accept(self, visitor):
        return visitor.visit_set(self)

class DictionaryNode(Node):

    def __init__(self, keys: list[Node] = None, values: list[Node] = None) -> None:
        self.keys: list[Node] = keys or []
        self.values: list[Node] = values or []

    def accept(self, visitor):
        return visitor.visit_dict(self)

class Boolean(Node):

    def __init__(self, value: bool) -> None:
        self.value: bool = value

    def accept(self, visitor):
        return visitor.visit_boolean(self)

class NoneNode(Node):
    def accept(self, visitor):
        return visitor.visit_none(self)

class Index(Node):

    def __init__(self, obj: Node, index: Node) -> None:
        self.obj: Node = obj
        self.index: Node = index

    def accept(self, visitor):
        return visitor.visit_index(self)

class Slice(Node):

    def __init__(self, obj: Node, start: Node | None = None, end: Node | None = None, step: Node | None = None) -> None:
        self.obj: Node = obj
        self.start: Node | None = start
        self.end: Node | None = end
        self.step: Node | None = step

    def accept(self, visitor):
        return visitor.visit_slice(self)

class Import(Node):

    def __init__(self, modules: list[Variable], aliases: list[Variable]= None) -> None:
        self.modules: list[Variable] = modules
        self.aliases: list[Variable] = aliases or []

    def accept(self, visitor):
        return visitor.visit_import(self)

class FromImport(Node):

    def __init__(self, path: Variable, modules: list[Variable], aliases: list[Variable] = None) -> None:
        self.path: Variable = path
        self.modules: list[Variable] = modules
        self.aliases: list[Variable] = aliases or []

    def accept(self, visitor):
        return visitor.visit_from_import(self)

class Raise(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

    def accept(self, visitor):
        return visitor.visit_raise(self)

class Break(Node):

    def accept(self, visitor):
        return visitor.visit_break()

class Continue(Node):

    def accept(self, visitor):
        return visitor.visit_continue()

class Pass(Node):

    def accept(self, visitor):
        return visitor.visit_pass()

class Yield(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

    def accept(self, visitor):
        return visitor.visit_yield(self)

class MatchNode(Node):

    def __init__(self, variable: Node, values: list[tuple[Node, Block]]) -> None:
        self.variable: Node = variable
        self.values: list[tuple[Node, Block]] = values

    def accept(self, visitor):
        return visitor.visit_match(self)

class AndNode(Node):

    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node =  left
        self.right: Node = right

    def accept(self, visitor):
        return visitor.visit_and(self)

class OrNode(Node):

    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node = left
        self.right: Node = right

    def accept(self, visitor):
        return visitor.visit_or(self)

class NotNode(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

    def accept(self, visitor):
        return visitor.visit_not(self)

class Operation(Node):

    def __init__(self, left: Node, right: Node, operator: str) -> None:
        self.left: Node = left
        self.right: Node = right
        self.operator: str = operator

    def accept(self, visitor):
        return visitor.visit_operation(self)

class InNode(Node):

    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node = left
        self.right: Node = right

    def accept(self, visitor):
        return visitor.visit_in(self)

class IsNode(Node):

    def __init__(self, left: Node, right: Node) -> None:
        self.left: Node = left
        self.right: Node = right

    def accept(self, visitor):
        return visitor.visit_is(self)

class KeyArg(Node):

    def __init__(self, variable: Variable, value: Node) -> None:
        self.variable: Node = variable
        self.value: Node = value

    def accept(self, visitor):
        return visitor.visit_keyarg(self)

class Program(Node):

    def __init__(self, block: Block = None) -> None:
        self.block: Block = Block([Pass()]) if not block or len(block.nodes) == 0 else block


class DelNode(Node):

    def __init__(self, value: Node) -> None:
        self.value: Node = value

    def accept(self, visitor):
        return visitor.visit_del(self)
