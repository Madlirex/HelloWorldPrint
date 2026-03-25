from scripts.constants import KEYWORDS_LIST, FLAT_KEYWORD_FUNCTIONS, KEYWORDS, SWAPPED_KEYWORDS, BRACKETS, BRACKET_PAIRS
from token import TokenType, Token
from tokenizer import Tokenizer
from node import *


# noinspection PyShadowingNames
class Parser:

    def __init__(self, tokenized_code: list[Token]) -> None:
        self.tokens: list[Token] = tokenized_code
        self.pos: int = 0
        self.expected_indent: int = -4

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
            tok = tokens[i] if i >= 0 else None

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

    def consume_words(self, tokens: list[Token], *words: str) -> int:

        if not self.match_words(tokens, *words):
            raise SyntaxError(f"Expected {' '.join(words)}, got {tokens}")
        return len(words)

    def find_words(self, tokens: list[Token], *words: str) -> int:
        for i in range(len(tokens)):
            if self.match_words(tokens[i:], *words):
                return i
        return -1

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

    #region Line Helpers

    def check_indent(self, token: Token) -> None:
        if token.token_type == TokenType.INDENT:
            if not token.value == self.expected_indent:
                raise IndentationError(f"Wrong indent {token.value}, expected {self.expected_indent}")

    def peek_curr_line(self) -> list[Token]:
        token_buffer: list[Token] = []
        i = 0
        while not self.is_at_end() and not self.peek(i).token_type == TokenType.NEWLINE:
            token_buffer.append(self.peek(i))
            i += 1
            if token_buffer[-1].token_type == TokenType.COMMENT:
                token_buffer.pop()

        return token_buffer

    def consume_curr_line(self) -> list[Token]:
        token_buffer: list[Token] = []
        while not self.is_at_end() and not self.peek().token_type == TokenType.NEWLINE:
            token_buffer.append(self.advance())
            if token_buffer[-1].token_type == TokenType.COMMENT:
                token_buffer.pop()

        return token_buffer

    #endregion

    #endregion

    #region Parsing

    #region Basics

    def parse_program(self) -> Program:

        program = Program(self.parse_block())

        return program

    def parse_tokens(self, tokens: list[Token]) -> Node | None:
        if len(tokens) == 1:
            return self.parse_single_token(tokens[0])

        if len(tokens) == 0:
            return None

        if tokens[-1].token_type.is_bracket:
            if tokens[-2].token_type == TokenType.COMMA or tokens[-2].token_type == TokenType.COLON:
                return self.parse_list_type(tokens)
            return self.parse_function(tokens)

        if tokens[1].token_type == TokenType.DOT:
            return self.parse_attribute(tokens)

        if tokens[1].token_type == TokenType.COMMA:
            return TupleNode(self.parse_token_list(tokens))

        if tokens[1].token_type == TokenType.OPERATOR:
            return self.parse_operator(tokens)

        return self.parse_logical_operator(tokens)

    def parse_line(self, line: list[Token]) -> Node:
        kw = self.peek_keyword(line)

        if kw == "if":
            return self.parse_if(line)
        if kw == "while":
            return self.parse_while(line)
        if kw == "def":
            return self.parse_def(line)
        if kw == "class":
            return self.parse_class(line)
        if kw == "for":
            return self.parse_for(line)

        for tok in line[::-1]:
            if tok.token_type == TokenType.EQUAL or tok.token_type == TokenType.EQUAL_OPERATOR:
                return self.parse_assignment(line)
            if tok.token_type == TokenType.RPAREN:
                return self.parse_function(line)

        raise NotImplementedError(f"Not implemented for {line}")

    def parse_block(self) -> Block:
        self.skip_redundant_newlines()
        self.expected_indent += 4

        past_statement: IfStatement | ForLoop | MatchNode | TryExcept | None = None

        nodes = []
        indent = self.peek().value if self.peek().token_type == TokenType.INDENT else self.peek(1).value
        while not self.is_at_end() and self.peek(1).value == indent:
            self.advance()
            self.check_indent(self.advance())

            token_buffer = self.consume_curr_line()
            if token_buffer:
                kw = self.peek_keyword(token_buffer)
                if kw == "elif":
                    past_statement.elifs.append(self.parse_elif(token_buffer))
                elif kw == "else":
                    past_statement.else_body = self.parse_else(token_buffer)
                elif kw == "case":
                    past_statement.values.append(self.parse_case(token_buffer))
                elif kw == "except":
                    past_statement.excepts.append(self.parse_except(token_buffer))
                else:
                    nodes.append(self.parse_line(token_buffer))

                if type(nodes[-1]) in (IfStatement, ForLoop, MatchNode, TryExcept):
                    past_statement = nodes[-1]

            self.skip_redundant_newlines()
        self.expected_indent -= 4
        return Block(nodes)

    def parse_assignment(self, tokens: list[Token]) -> Assignment:

        left = []
        right = []
        op = ""

        for i in reversed(range(len(tokens))):
            if tokens[i].token_type == TokenType.EQUAL_OPERATOR or tokens[i].token_type == TokenType.EQUAL:
                op = tokens[i].value
                left = self.parse_token_list(tokens[0:i], ";")
                right = self.parse_token_list(tokens[i+1:], ";")
                break

        return Assignment(right, left, op)

    def parse_function(self, tokens: list[Token]) -> Call:
        start = 0
        for i, token in enumerate(reversed(tokens)):
            if token.token_type == TokenType.LPAREN:
                start = len(tokens) - i
                break

        end = -1

        name = self.parse_tokens(tokens[start:end])
        args = self.parse_token_list(tokens[:start-1:], ",")

        return Call(name, args)

    def parse_attribute(self, tokens: list[Token]) -> Attribute:
        obj = self.parse_tokens(tokens[:-2])
        name = tokens[-1].value
        return Attribute(obj, name)

    def parse_operator(self, tokens: list[Token]) -> Operation:
        left = self.parse_single_token(tokens[0])
        right = self.parse_single_token(tokens[2])
        return Operation(left, right, tokens[1].value)

    #endregion

    #region Simple Keywords

    #endregion

    #region Logical Operators

    def parse_logical_operator(self, tokens: list[Token]) -> Node:
        kw = self.peek_keyword(tokens)

        if kw == "not":
            return self.parse_not(tokens)

        kw = self.peek_keyword(tokens[1:])

        if kw == "or":
            return self.parse_or(tokens)
        if kw == "and":
            return self.parse_and(tokens)
        if kw in ("<", ">", "<=", ">=", "!=", "=="):
            return self.parse_equality(tokens, kw)
        if kw == "in":
            return self.parse_in(tokens)
        if kw == "is":
            return self.parse_is(tokens)

        raise NotImplementedError(f"Not implemented for tokens {tokens}")

    def parse_not(self, tokens: list[Token]) -> NotNode:
        start = self.consume_words(tokens, *SWAPPED_KEYWORDS['not'])

        return NotNode(self.parse_tokens(tokens[start:]))

    def parse_or(self, tokens: list[Token]) -> OrNode:
        start = self.find_words(tokens, *SWAPPED_KEYWORDS['or'])
        end = start + len(SWAPPED_KEYWORDS['or'])

        if start != -1:
            return OrNode(self.parse_tokens(tokens[:start]), self.parse_tokens(tokens[end::]))

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS} to be in {tokens}")

    def parse_and(self, tokens: list[Token]) -> OrNode:
        start = self.find_words(tokens, *SWAPPED_KEYWORDS['and'])
        end = start + len(SWAPPED_KEYWORDS['and'])

        if start != -1:
            return OrNode(self.parse_tokens(tokens[:start]), self.parse_tokens(tokens[end::]))

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS} to be in {tokens}")

    def parse_equality(self, tokens: list[Token], operator: str) -> Operation:
        start = self.find_words(tokens, *SWAPPED_KEYWORDS[operator])
        end = start + len(SWAPPED_KEYWORDS[operator])

        if start != -1:
            return Operation(self.parse_tokens(tokens[:start]), self.parse_tokens(tokens[end::]), operator)

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS} to be in {tokens}")

    def parse_in(self, tokens: list[Token]) -> InNode:
        start = self.find_words(tokens, *SWAPPED_KEYWORDS['in'])
        end = start + len(SWAPPED_KEYWORDS['in'])

        if start != -1:
            return InNode(self.parse_tokens(tokens[:start]), self.parse_tokens(tokens[end::]))

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS} to be in {tokens}")

    def parse_is(self, tokens: list[Token]) -> IsNode:
        start = self.find_words(tokens, *SWAPPED_KEYWORDS['is'])
        end = start + len(SWAPPED_KEYWORDS['is'])

        if start != -1:
            return IsNode(self.parse_tokens(tokens[:start]), self.parse_tokens(tokens[end::]))

        raise SyntaxError(f"Expected {SWAPPED_KEYWORDS} to be in {tokens}")
    #endregion

    #region Data Types

    def parse_single_token(self, token: Token) -> Node:

        if self.check_words([token], *SWAPPED_KEYWORDS['None']):
            return NoneNode()
        if self.check_words([token], *SWAPPED_KEYWORDS['True']):
            return Boolean(True)
        if self.check_words([token], *SWAPPED_KEYWORDS['False']):
            return Boolean(False)

        if token.token_type == TokenType.STRING:
            return String(token.value)
        if token.token_type == TokenType.NUMBER:
            return Number(token.value)
        if token.token_type == TokenType.VALUE:
            return Variable(token.value)

        raise Exception(f"Unexpected tokens: {token}")

    def parse_list_type(self, values: list[Token]) -> Node:
        bracket = values[0].value
        if bracket in "{}":
            return self.parse_braces(values)
        if bracket in "[]":
            return ListNode(self.parse_token_list(values))
        if bracket in "()":
            return TupleNode(self.parse_token_list(values))

        raise NotImplementedError("Not implemented list type")

    def parse_braces(self, tokens: list[Token]) -> Node:
        pass

    def parse_token_list(self, values: list[Token], sep: str = ",") -> list[Node]:

        result = []
        open_brackets = []
        token_buffer = []

        for token in values:
            token_buffer.append(token)

            if token.token_type.is_opening_bracket:
                open_brackets.append(token.value)
            elif token.token_type.is_bracket:
                if len(open_brackets) > 0 and BRACKET_PAIRS[token.value] == open_brackets[-1]:
                    open_brackets.pop()
                else:
                    raise Exception("Not enough brackets to close")

            if len(open_brackets) == 0:
                if token.value == sep:
                    token_buffer.pop()
                    result.append(self.parse_tokens(token_buffer))
                    token_buffer = []

        result.append(self.parse_tokens(token_buffer))

        return result


    #endregion

    #region Advanced Keywords

    def parse_if(self, tokens: list[Token]) -> IfStatement:
        self.consume_words(tokens, *SWAPPED_KEYWORDS['if'])

        if tokens[-1].token_type != TokenType.QUESTION:
            raise SyntaxError("Invalid syntax you illiterate swine")

        body = self.parse_block()

        return IfStatement(self.parse_tokens(tokens[len(SWAPPED_KEYWORDS['if']):-1:]), body)

    def parse_elif(self, tokens: list[Token]) -> tuple[Node, Block]:
        start = self.consume_words(tokens, *SWAPPED_KEYWORDS['elif'])

        if tokens[-1].token_type != TokenType.QUESTION:
            raise SyntaxError("Invalid syntax you illiterate swine")

        return self.parse_tokens(tokens[start:-1]), self.parse_block()

    def parse_else(self, tokens: list[Token]) -> Block:
        if tokens[-1].token_type != TokenType.EXCLAMAITON:
            raise SyntaxError("Invalid syntax you illiterate swine")

        return self.parse_block()

    def parse_while(self, tokens: list[Token]) -> While:
        self.consume_words(tokens, *SWAPPED_KEYWORDS['while'])

        if tokens[-1].token_type != TokenType.EXCLAMAITON:
            raise SyntaxError("Invalid syntax you illiterate swine")

        return While(self.parse_tokens(tokens[len(SWAPPED_KEYWORDS['while']):-1:]), self.parse_block())

    def parse_def(self, tokens: list[Token]) -> FunctionDef:
        start = self.consume_words(tokens, *SWAPPED_KEYWORDS['def'])

        if tokens[-1].token_type != TokenType.DOT:
            raise SyntaxError("Invalid syntax you illiterate swine")

        name = tokens[start].value
        params = self.parse_token_list(tokens[start+2:-2])
        return FunctionDef(name, self.parse_block(), params)

    def parse_class(self, tokens: list[Token]) -> ClassDef:
        start = self.consume_words(tokens, *SWAPPED_KEYWORDS['class'])

        if tokens[-1].token_type != TokenType.DOT:
            raise SyntaxError("Invalid syntax you illiterate swine")

        name = tokens[start].value
        parents = self.parse_token_list(tokens[start+2:-2])
        return ClassDef(name, self.parse_block(), parents)

    def parse_for(self, tokens: list[Token]) -> ForLoop:
        start = self.consume_words(tokens, *SWAPPED_KEYWORDS['for'])

        if tokens[-1].token_type != TokenType.EXCLAMAITON:
            raise SyntaxError("Invalid syntax you illiterate swine")

        end = 0
        for i in reversed(range(len(tokens))):
            if self.match_words(tokens[i:], *SWAPPED_KEYWORDS['in']):
                end = i

        variables = self.parse_token_list(tokens[start:end])
        expression = self.parse_tokens(tokens[end+len(SWAPPED_KEYWORDS['in']):-1])

        return ForLoop(variables, expression, self.parse_block())

    #endregion

    #region Miscellaneous

    #endregion

    #endregion
"""
code = open("../tests/helloworld.print", 'r', encoding='utf8').read()

tokens = Tokenizer(code).tokenize()

#print("TOKENS:")
#print(tokens)

parser = Parser(tokens)

ast = parser.parse_program()

print("\nAST:")
print(ast.block.nodes)
"""