from contextlib import contextmanager

from node import *


# noinspection PyMethodMayBeStatic
class Transpiler:

    def __init__(self, ast: Program) -> None:
        self.ast: Program = ast
        self.pos: int = 0
        self.indent: int = 0
        self.indent_size: int = 4

    def transpile_program(self) -> str:
        result = ""
        for line in self.ast.block.nodes:
            result += f"{self.transpile(line)}\n"

        return result

    def transpile_nodes(self, nodes: list[Node] | tuple[Node, ...]) -> str:
        return ", ".join(self.transpile(node) for node in nodes)

    def transpile(self, node: Node) -> str:
        return node.accept(self)

    def emit(self, text: str) -> str:
        return (self.indent * self.indent_size) * " " + text

    @contextmanager
    def indented(self):
        self.indent += 1
        try:
            yield
        finally:
            self.indent -= 1

    #region Visits

    #region Basics

    def visit_block(self, node: Block) -> str:

        result = ''

        # noinspection PyArgumentList
        with self.indented():
            for stmt in node.nodes:
                print(type(stmt))
                result += self.emit(self.transpile(stmt) + "\n")

        return result

    def visit_assignment(self, node: Assignment) -> str:

        return f"{self.transpile_nodes(node.left)} = {self.transpile_nodes(node.right)}"

    def visit_attribute(self, node: Attribute) -> str:
        return f"{self.transpile(node.obj)}.{node.name}"

    def visit_call(self, node: Call) -> str:
        return f"{node.func}({self.transpile_nodes(node.args)})"

    #endregion

    #region Simple Keywords

    def visit_pass(self) -> str:
        return "pass"

    def visit_continue(self) -> str:
        return "continue"

    def visit_break(self) -> str:
        return "break"

    def visit_return(self, node: Return) -> str:
        return f"return {self.transpile(node.value)}"

    #endregion

    #region Logical Expressions

    def visit_in(self, node: InNode) -> str:
        return f"{self.transpile(node.left)} in {self.transpile(node.right)}"

    def visit_is(self, node: IsNode) -> str:
        return f"{self.transpile(node.left)} is {self.transpile(node.right)}"

    def visit_or(self, node: OrNode) -> str:
        return f"{self.transpile(node.left)} or {self.transpile(node.right)}"

    def visit_and(self, node: AndNode) -> str:
        return f"{self.transpile(node.left)} and {self.transpile(node.right)}"

    def visit_not(self, node: NotNode) -> str:
        return f"not {self.transpile(node.value)}"

    def visit_operation(self, node: Operation) -> str:
        return f"{self.transpile(node.left)} {node.operator} {self.transpile(node.right)}"

    #endregion

    #region Data Types

    def visit_none(self, node: NoneNode) -> str:
        return "None"

    def visit_bool(self, node: Boolean) -> str:
        return str(node.value)

    def visit_number(self, node: Number) -> str:
        return str(node.value)

    def visit_string(self, node: String) -> str:
        return node.value

    def visit_variable(self, node: Variable) -> str:
        return node.name

    def visit_list(self, node: ListNode) -> str:
        return f"[{self.transpile_nodes(node.values)}]"

    def visit_tuple(self, node: TupleNode) -> str:
        return f"({self.transpile_nodes(node.values)},)"

    def visit_set(self, node: SetNode) -> str:
        return "{" + self.transpile_nodes(node.values) + "}"

    def visit_dict(self, node: DictionaryNode) -> str:

        result: str = "{"

        try:
            for i in range(len(node.keys)):
                result += f"{node.keys[i]}: {node.values[i]}, "
        except IndexError:
            raise ValueError(f"Not enough values to unpack from dictionary. There are more keys than values.")

        result = result[:-2:] if result.endswith(", ") else result
        result += "}"

        return result

    #endregion

    #region Advanced Keywords

    def visit_if(self, node: IfStatement) -> str:
        result = f"if {self.transpile(node.condition)}:\n"

        result += self.visit_block(node.body)

        for elseif in node.elifs:
            result += self.visit_elif(elseif)

        result += self.visit_else(node.else_body)

        return result

    def visit_elif(self, node: tuple[Node, Block]) -> str:
        return self.emit(f"elif {self.transpile(node[0])}:\n") + self.visit_block(node[1])

    def visit_else(self, body: Block) -> str:
        return self.emit("else:\n") + self.visit_block(body)

    def visit_while(self, node: While) -> str:
        result = f"while {self.transpile(node.condition)}:\n"

        result += self.visit_block(node.body)

        return result

    def visit_class(self, node: ClassDef) -> str:

        result = f"class {node.name}({self.transpile_nodes(node.parents)}):\n"
        result += self.visit_block(node.body)

        return result

    def visit_function(self, node: FunctionDef) -> str:

        result = f"def {node.name}({self.transpile_nodes(node.params)}):\n"
        result += self.visit_block(node.body)

        return result

    def visit_try(self, node: TryExcept) -> str:

        result = "try:\n"
        result += self.visit_block(node.body)
        for except_node in node.excepts:
            result += self.visit_except(except_node)
        return result

    def visit_except(self, node: tuple[Node, Block]) -> str:

        result = f"except {self.transpile(node[0])}:\n"
        result += self.visit_block(node[1])
        return result

    def visit_for(self, node: ForLoop) -> str:

        result = f"for {self.transpile_nodes(node.variable)} in {self.transpile(node.expression)}:\n"
        result += self.visit_block(node.body)
        result += self.visit_else(node.else_body)
        return result

    def visit_lambda(self, node: Lambda) -> str:
        return f"lambda {self.transpile_nodes(node.params)}: {self.transpile(node.body)}"

    def visit_ternary(self, node: TernaryOp) -> str:
        return f"{self.transpile(node.value1)} if {self.transpile(node.condition)} else {self.transpile(node.value2)}"

    def visit_list_comp(self, node: ListComprehension) -> str:

        result = f"{self.transpile_nodes(node.body)} for {self.transpile_nodes(node.variable)} in {self.transpile(node.expression)}"
        result += f"if {self.transpile(node.filter)}" if node.filter else ""
        return result

    #endregion

    #endregion

pr = Program()
pr.block = Block([IfStatement(Variable("Hi"), Block([Assignment([Variable("Hi")], [String("Hello")])])), Assignment([Variable("Hi")], [String("Hello")])])
pr.block = Block([FunctionDef("SampleFunction", pr.block, [Variable("Fucker"), Variable("sucker")])])
pr.block = Block([ClassDef("SampleClass", pr.block)])
trans = Transpiler(pr)
print(trans.transpile_program())