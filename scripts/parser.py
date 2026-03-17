from scripts.constants import KEYWORDS_LIST, FLAT_KEYWORD_FUNCTIONS, KEYWORDS, SWAPPED_KEYWORDS, PRECEDENCE
from token import TokenType, Token
from tokenizer import Tokenizer
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

    def peek_keyword(self) -> str | None:

        for words, replacement in KEYWORDS_LIST:
            if self.check_words(*words):
                return replacement

        return None

    def consume_keyword(self) -> str | None:

        for words, replacement in KEYWORDS_LIST:
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

        program.nodes = self.parse_block()

        return program

    def parse_block(self) -> list[Node]:

        block = []
        indent = self.peek().value

        while self.peek().value == indent and not self.is_at_end():
            self.parse()

        return block

    def parse(self) -> Node:

        if self.peek(0).token_type == TokenType.INDENT:
            self.advance()

        kw = self.peek_keyword()

        if kw == "if":
            return self.parse_if()

        return self.parse_expression()

    def parse_expression(self) -> Node:
        pass

    def parse_if(self) -> IfStatement:
        self.consume_words(*SWAPPED_KEYWORDS['if'])

        condition = self.parse_expression()
        self.consume(TokenType.QUESTION)
        body = self.parse_block()

        elifs = []
        is_elif = self.check_words(*SWAPPED_KEYWORDS['elif'])

        while is_elif:
            self.consume_words(*SWAPPED_KEYWORDS['elif'])
            cond = self.parse_expression()
            self.consume(TokenType.QUESTION)
            elifs.append((cond, self.parse_block()))

        else_body = []
        if self.check_words(*SWAPPED_KEYWORDS['else']):
            self.consume_words(*SWAPPED_KEYWORDS['else'])
            self.consume(TokenType.EXCLAMAITON)
            else_body = self.parse_block()

        return IfStatement(condition, body, elifs, else_body)


code = open("../tests/helloworld.print", 'r', encoding='utf8').read()

tokens = Tokenizer(code).tokenize()

#print("TOKENS:")
#print(tokens)

parser = Parser(tokens)

ast = parser.parse_program()

print("\nAST:")
#print("\n".join(ast.nodes))