from token import TokenType, Token
from tokenizer import Tokenizer
from node import *

class Parser:

    def __init__(self, tokenized_code: list[Token]) -> None:
        self.tokens: list[Token] = tokenized_code
        self.pos: int = 0

    def peek(self, x: int = 1) -> Token | None:

        if 0 > self.pos + x >= len(self.tokens):
            return None

        return self.tokens[self.pos + x]

    def advance(self) -> Token | None:

        if self.pos < len(self.tokens):
            self.pos += 1

        return self.peek(-1)

    def check(self, tok_type: TokenType) -> bool:

        tok: Token = self.peek()

        return tok is not None and tok.token_type == tok_type

    def match(self, tok_type: TokenType) -> bool:

        if self.check(tok_type):
            self.advance()
            return True

        return False

    def consume(self, tok_type: TokenType) -> Token:

        if self.check(tok_type):
            return self.advance()

        raise SyntaxError(f"Expected {tok_type}, got {self.peek().token_type}")

    def is_at_end(self) -> bool:

        return self.peek().token_type == TokenType.EOF

    def parse(self) -> Program:

        program = Program()

        while not self.is_at_end():
            program.nodes.append(str(self.advance().value))

        return program

code = open("../tests/helloworld.print", 'r', encoding='utf8').read()

tokens = Tokenizer(code).tokenize()

print("TOKENS:")
print(tokens)

parser = Parser(tokens)

ast = parser.parse()

print("\nAST:")
print("\n".join(ast.nodes))