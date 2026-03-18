from scripts.constants import KEYWORDS_LIST, FLAT_KEYWORD_FUNCTIONS, KEYWORDS, SWAPPED_KEYWORDS
from token import TokenType, Token
from tokenizer import Tokenizer
from node import *

class Parser:

    def __init__(self, tokenized_code: list[Token]) -> None:
        self.tokens: list[Token] = tokenized_code
        self.pos: int = 0

    #region Helpers
    #region Basic Helpers

    def peek(self, x: int = 0) -> Token | None:
        pos = self.pos + x

        if pos < 0 or pos >= len(self.tokens):
            return None

        return self.tokens[pos]

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

    def skip_redundant_newlines(self) -> None:

        while not self.is_at_end() and self.peek(2).token_type == TokenType.NEWLINE:

            self.consume(TokenType.NEWLINE)
            self.consume(TokenType.INDENT)

    #endregion

    #region Words Helpers

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
            raise SyntaxError(f"Expected {' '.join(words)}, got {self.peek().value}")

    #endregion

    #region Keyword Helpers

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

    #endregion

    #endregion

    def parse_program(self) -> Program:

        program = Program()

        program.nodes = self.parse_block()

        return program

    def parse(self) -> Node:

        if self.peek().token_type == TokenType.INDENT:
            self.advance()

        kw = self.peek_keyword()

        if kw == "if":
            return self.parse_if()

        return self.parse_expression()

    def parse_block(self) -> Block:

        self.skip_redundant_newlines()

        nodes = []
        indent = self.peek().value

        while self.peek(1).value == indent and not self.is_at_end():
            self.advance()
            self.advance()

            nodes.append(self.parse())

            self.skip_redundant_newlines()

        return Block(nodes)

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

        return IfStatement(condition, body, elifs, self.parse_else())

    def parse_else(self) -> list[Node] | None:
        body = None
        if self.check_words(*SWAPPED_KEYWORDS['else']):
            self.consume_words(*SWAPPED_KEYWORDS['else'])
            self.consume(TokenType.EXCLAMAITON)
            body = self.parse_block()
        return body

    def parse_while(self) -> While:
        self.consume_words(*SWAPPED_KEYWORDS['while'])

        condition = self.parse_expression()
        self.consume(TokenType.EXCLAMAITON)
        body = self.parse_block()

        return While(condition, body)

    def parse_for(self) -> ForLoop:
        self.consume_words(*SWAPPED_KEYWORDS['for'])

        variable = self.parse_variables()

        self.consume_words(*SWAPPED_KEYWORDS['in'])

        expression = self.parse_expression()
        self.consume(TokenType.EXCLAMAITON)
        body = self.parse_block()

        return ForLoop(variable, expression, body, self.parse_else())

    def parse_variables(self) -> list[Variable]:

        nodes = [Variable(self.consume(TokenType.VALUE).value)]

        while self.check(TokenType.COMMA):
            self.consume(TokenType.COMMA)
            nodes.append(Variable(self.consume(TokenType.VALUE).value))

        return nodes

    def parse_def(self) -> FunctionDef:

        name = self.consume(TokenType.VALUE).value
        self.consume(TokenType.LPAREN)
        params = self.parse_params()

        body = self.parse_block()
        return FunctionDef(name, body, params)

    def parse_params(self) -> list[Node]:
        pass

    def parse_class(self) -> ClassDef:

        name = self.consume(TokenType.VALUE).value
        self.consume(TokenType.LPAREN)
        parents = self.parse_parents()

        body = self.parse_block()
        return ClassDef(name, body, parents)

    def parse_parents(self) -> list[Node]:
        pass

code = open("../tests/helloworld.print", 'r', encoding='utf8').read()

tokens = Tokenizer(code).tokenize()

#print("TOKENS:")
#print(tokens)

parser = Parser(tokens)

ast = parser.parse_program()

print("\nAST:")
#print("\n".join(ast.nodes))