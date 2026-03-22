from scripts.constants import KEYWORDS_LIST, FLAT_KEYWORD_FUNCTIONS, KEYWORDS, SWAPPED_KEYWORDS, BRACKETS, BRACKET_PAIRS
from token import TokenType, Token
from tokenizer import Tokenizer
from node import *


# noinspection PyShadowingNames
class Parser:

    def __init__(self, tokenized_code: list[Token]) -> None:
        self.tokens: list[Token] = tokenized_code
        self.pos: int = 0

    #region Helpers
    #region Basic Helpers

    @staticmethod
    def reverse_sep(sep: str) -> str:
        return "," if sep == ";" else ";"

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

    def check_words(self, tokens: list[Token], *words: str) -> bool:

        for i, word in enumerate(words):
            tok = tokens[i]

            if tok is None:
                return False

            if tok.token_type != TokenType.VALUE:
                return False

            if tok.value != word:
                return False

        return True

    def match_words(self, tokens: list[Token], *words: str) -> bool:

        if not self.check_words(tokens, *words):
            return False

        return True

    def consume_words(self, tokens: list[Token], *words: str) -> None:

        if not self.match_words(tokens, *words):
            raise SyntaxError(f"Expected {' '.join(words)}, got {tokens}")

    #endregion

    #region Keyword Helpers

    def peek_keyword(self, tokens: list[Token]) -> str | None:

        for words, replacement in KEYWORDS_LIST:
            if self.check_words(tokens, *words):
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

    #region Parsing

    #region Basics

    def parse_program(self) -> Program:

        program = Program(self.parse_block())

        return program

    def parse_line(self, line: list[Token]) -> Node:
        kw = self.peek_keyword(line)

        if kw == "if":
            return self.parse_if()
        if kw == "while":
            return self.parse_while()

        is_function = False
        for tok in line[::-1]:
            if tok.token_type == TokenType.EQUAL or tok.token_type == TokenType.EQUAL_OPERATOR:
                return self.parse_assignment(line)
            if tok.token_type == TokenType.RPAREN:
                return self.parse_function(line)

        raise NotImplementedError(f"Not implemented for {line}")

    def parse_block(self) -> Block:

        self.skip_redundant_newlines()

        nodes = []
        indent = self.peek().value if self.peek().token_type == TokenType.INDENT else self.peek(1).value
        while self.peek(1).value == indent and not self.is_at_end():
            self.advance()
            self.advance()

            token_buffer = []

            while not self.peek().token_type == TokenType.NEWLINE:
                token_buffer.append(self.advance())

            nodes.append(self.parse_line(token_buffer))

            self.skip_redundant_newlines()

        return Block(nodes)

    def parse_assignment(self, tokens: list[Token]) -> Assignment:

        left = []
        right = []
        op = ""

        for i in reversed(range(len(tokens))):
            if tokens[i].token_type == TokenType.EQUAL_OPERATOR or tokens[i].token_type == TokenType.EQUAL:
                op = tokens[i].value
                left = self.parse_list(tokens[0:i])
                right = self.parse_list(tokens[i+1:])

        return Assignment(right, left, op)

    def parse_function(self, tokens: list[Token]) -> Call:

        name = self.parse_token([tokens[-2]])
        args = []
        for arg in tokens:
            pass

        return Call()

    #endregion

    #region Simple Keywords

    #endregion

    #region Logical Operators

    #endregion

    #region Data Types

    def parse_token(self, tokens: list[Token]) -> Node:

        if self.check_words(tokens, *SWAPPED_KEYWORDS['None']):
            return NoneNode()
        if self.check_words(tokens, *SWAPPED_KEYWORDS['True']):
            return Boolean(True)
        if self.check_words(tokens, *SWAPPED_KEYWORDS['False']):
            return Boolean(False)
        if len(tokens) == 1:
            if tokens[0].token_type == TokenType.STRING:
                return String(tokens[0].value)
            if tokens[0].token_type == TokenType.NUMBER:
                return Number(tokens[0].value)
            if tokens[0].token_type == TokenType.VALUE:
                return Variable(tokens[0].value)

        raise Exception(f"Unexpected tokens: {tokens}")

    def parse_list_type(self, values: list[Token], sep: str = ",", bracket: str = "[") -> Node:
        sep = self.reverse_sep(sep)
        if bracket in "{}":
            return self.parse_braces(values, sep)
        if bracket in "[]":
            return ListNode(self.parse_list(values, sep))
        if bracket in "()":
            return TupleNode(self.parse_list(values, sep))

        raise NotImplementedError("Not implemented list type")

    def parse_braces(self, tokens: list[Token], sep: str = ",") -> Node:
        pass

    def parse_list(self, values: list[Token], sep: str = ",") -> list[Node]:

        open_brackets = []
        token_buffer: list[Token] = []
        result = []
        for token in values:
            if token.token_type.is_opening_bracket:
                open_brackets += token.value
                token_buffer.append(token)

            if not open_brackets:
                print(token)
                if token.value == sep:
                    result.append(self.parse_token(token_buffer))
                else:
                    token_buffer.append(token)
            else:
                if token.value in BRACKET_PAIRS:
                    if BRACKET_PAIRS[token.value] == open_brackets[-1]:
                        open_brackets.pop()
                        if not open_brackets:
                            result.append(self.parse_list_type(token_buffer, sep, token.value))
                    else:
                        raise Exception("Unclosed bracket.")
                else:
                    token_buffer.append(token)

        return result


    #endregion

    #region Advanced Keywords

    def parse_if(self) -> IfStatement:
        pass

    def parse_while(self) -> While:
        pass

    #endregion

    #region Miscellaneous

    def parse_params(self) -> list[Node]:
        pass

    def parse_parents(self) -> list[Node]:
        pass

    #endregion

    #endregion

code = open("../tests/helloworld.print", 'r', encoding='utf8').read()

tokens = Tokenizer(code).tokenize()

#print("TOKENS:")
#print(tokens)

parser = Parser(tokens)

ast = parser.parse_program()

print("\nAST:")
print(ast.block.nodes)
print(ast.block.nodes[0].__dict__)
print(ast.block.nodes[0].right[0].__dict__)