from token import TokenType
from tokenizer import Tokenizer
from node import *

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):

        statements = []
        while self.peek().token_type != TokenType.EOF:
            statements.append(self.parse_expression())
        p = Program()
        p.nodes = statements
        return p

    def parse_expression(self, precedence=0):

        token = self.advance()
        left = self.nud(token)

        while precedence < self.get_precedence():
            token = self.advance()
            left = self.led(token, left)

        return left

    def nud(self, token):

        if token.token_type == TokenType.VALUE:
            return Variable(token.value)

        if token.token_type == TokenType.NUMBER:
            return Number(token.value)

        if token.token_type == TokenType.STRING:
            return String(token.value)

        if token.token_type == TokenType.LPAREN:
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        raise Exception("Unexpected token")

    def led(self, token, left):

        if token.token_type == TokenType.EQUAL:

            right = self.parse_expression(9)
            return Assignment(left, right)

        if token.token_type == TokenType.DOT:

            name = self.advance()
            return Attribute(left, name.value)

        if token.token_type == TokenType.LPAREN:

            args = []

            if self.peek().token_type != TokenType.RPAREN:

                while True:

                    args.append(self.parse_expression())

                    if self.peek().token_type != TokenType.COMMA:
                        break

                    self.advance()

            self.expect(TokenType.RPAREN)

            return Call(left, args)

        raise Exception("Unknown operator")

    def get_precedence(self):

        if self.pos >= len(self.tokens):
            return 0

        tok = self.peek()

        table = {
            TokenType.EQUAL: 10,
            TokenType.LPAREN: 40,
            TokenType.DOT: 50
        }

        return table.get(tok.token_type, 0)

    def expect(self, t):

        tok = self.advance()

        if tok.token_type != t:
            raise Exception("Unexpected token")


code = open("../tests/helloworld.print", 'r', encoding='utf8').read()

tokens = Tokenizer(code).tokenize()

print("TOKENS:")
print(tokens)

parser = Parser(tokens)

ast = parser.parse()

print("\nAST:")
print("\n".join(ast.nodes))