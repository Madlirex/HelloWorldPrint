from contextlib import contextmanager

from node import *


# noinspection PyArgumentList
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
    def visit_if(self, node: IfStatement) -> str:
        result = self.emit(f"if {self.transpile(node.condition)}:\n")

        with self.indented():
            for stmt in node.body.nodes:
                result += self.transpile(stmt) + "\n"

        return result

    def visit_while(self, node: While) -> str:
        result = self.emit(f"while {self.transpile(node.condition)}:\n")

        with self.indented():
            for stmt in node.body.nodes:
                result += self.transpile(stmt) + "\n"

        return result


    def visit_assignment(self, node: Assignment) -> str:

        left = ", ".join(self.transpile(i) for i in node.left)
        right = ", ".join(self.transpile(i) for i in node.right)

        return self.emit(f"{left}{node.operator}{right}")

    #endregion

pr = Program()
pr.block = Block([IfStatement(Variable("Hi"), Block([Assignment([Variable("Hi")], [String("Hello")])])), Assignment([Variable("Hi")], [String("Hello")])])

trans = Transpiler(pr)
print(trans.transpile_program())