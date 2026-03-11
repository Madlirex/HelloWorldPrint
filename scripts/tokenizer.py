from token import Token, TokenType
from constants import BRACKETS

class Tokenizer:

    def __init__(self, code: str) -> None:
        self.code: str = code
        self.pos: int = 0
        self.tokens: list[Token] = []
        self.curr_quotes: str = ''

    def peek(self, x: int = 0) -> str | None:
        if self.pos + x >= len(self.code):
            return None
        return self.code[self.pos + x]

    def advance(self) -> str:
        if self.pos >= len(self.code):
            return ""
        char = self.code[self.pos]
        self.pos += 1
        return char

    def tokenize(self) -> list[Token]:

        while self.pos < len(self.code):

            char = self.peek()
            print(char)
            if char == "\n":
                self.tokens.append(self.read_new_line())
                self.tokens.append(self.read_indent())
                continue

            if char.isspace():
                self.advance()
                continue

            if char.isdigit():
                self.tokens.append(self.read_number())
                continue

            if char.isalpha() or char == "_":
                self.tokens.append(self.read_identifier())
                continue

            if char == '"' or char == "'":
                self.tokens.append(self.read_string())
                continue

            if char == ".":
                self.tokens.append(Token(TokenType.DOT, char))
                self.advance()
                continue

            if char == "=":
                self.tokens.append(Token(TokenType.EQUAL, char))
                self.advance()
                continue

            if char == ",":
                self.tokens.append(Token(TokenType.COMMA, char))
                self.advance()
                continue

            if char in BRACKETS:
                self.tokens.append(Token(BRACKETS[char], char))
                self.advance()
                continue

            if char == "?":
                self.tokens.append(Token(TokenType.QUESTION, char))
                self.advance()
                continue

            if char == "!":
                self.tokens.append(Token(TokenType.EXCLAMAITON, char))
                self.advance()
                continue

            if char == ":":
                self.tokens.append(Token(TokenType.COLON, char))
                self.advance()
                continue

            if char == "#":
                self.tokens.append(self.read_comment())
                continue

            raise Exception(f"Unknown char {char}")

        self.tokens.append(Token(TokenType.EOF))
        return self.tokens

    def read_new_line(self) -> Token:
        return Token(TokenType.NEWLINE, self.advance())

    def read_indent(self) -> Token:

        value = 0

        while self.peek() == " ":
            value += 1
            self.advance()

        return Token(TokenType.INDENT, value)

    def read_comment(self) -> Token:

        value = ""
        while self.peek() != "\n" and self.peek():
            value += self.advance()

        return Token(TokenType.COMMENT, value)

    def read_number(self) -> Token:

        num = ""

        while self.peek() and self.peek().isdigit():
            num += self.advance()

        return Token(TokenType.NUMBER, int(num))

    def read_identifier(self) -> Token:

        name = ""

        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            name += self.advance()

        return Token(TokenType.VALUE, name)

    def read_multi_comment(self) -> Token:

        value = self.advance()
        quote_count = 0

        while quote_count < 3:
            value += self.advance()
            quote_count = quote_count + 1 if value[-1] == '"' else 0

        return Token(TokenType.COMMENT, value)

    def read_string(self) -> Token:

        value = self.peek()

        if self.peek() == self.peek(1) and self.peek() == value and value == '"':
            return self.read_multi_comment()

        value = self.advance()
        self.curr_quotes = value

        while self.peek() != self.curr_quotes:
            value += self.advance()

        value += self.advance()

        return Token(TokenType.STRING, value)

if __name__ == "__main__":
    data = open("../tests/helloworld.print", 'r', encoding='utf-8').read()
    tokenizer = Tokenizer(data)
    for token in tokenizer.tokenize():
        print(token)