from token import TokenType, Token
from tokenizer import Tokenizer
from constants import KEYWORD_FUNCTIONS
from node import *

class Parser:

    def __init__(self, tokenized_code: list[Token]) -> None:
        self.tokens: list[Token] = tokenized_code
        self.pos: int = 0

    def peek(self, x: int = 1) -> Token | None:
        pos = self.pos + x

        if pos < 0 or pos >= len(self.tokens):
            return None

        return self.tokens[pos]

    def check_words(self, *words: str) -> bool:

        for i, word in enumerate(words):
            tok = self.peek(i)

            if tok is None:
                return False

            if tok.token_type != TokenType.VALUE:
                return False

            if tok.value != word:
                return False

        return True

    def match_words(self, *words: str) -> bool:

        if not self.check_words(*words):
            return False

        for _ in words:
            self.advance()

        return True

    def consume_words(self, *words: str) -> None:

        if not self.match_words(*words):
            raise SyntaxError(f"Expected {' '.join(words)}, got {self.peek(0).value}")

    def get_keyword(self) -> str | None:

        for words, replacement in sorted(KEYWORD_FUNCTIONS.items(), key=lambda x: -len(x[0])):
            if self.check_words(*words):
                for _ in words:
                    self.advance()
                return replacement

        return None

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

    def parse_program(self) -> Program:

        program = Program()

        while not self.is_at_end():
            program.nodes.append(self.parse(self.peek(0)))

        return program

    def parse(self, token: Token) -> Node:

        pass
        # parse_if
        # parse_while

code = open("../tests/helloworld.print", 'r', encoding='utf8').read()

tokens = Tokenizer(code).tokenize()

print("TOKENS:")
print(tokens)

parser = Parser(tokens)

ast = parser.parse_program()

print("\nAST:")
print("\n".join(ast.nodes))