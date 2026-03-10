from enum import IntEnum

from position import PositionRange


class TokenType(IntEnum):

    VALUE = 0

    OPERATION = 1

    KEYWORD = 2

    LPAREN = 3
    RPAREN = 4
    LBRACKET = 5
    RBRACKET = 6
    LBRACE = 7
    RBRACE = 8
    COMMA = 9
    COLON = 10

    NEWLINE = 11
    INDENT = 12
    COMMENT = 13

    FUNCTION = 14

    UNKNOWN = 15

    @property
    def is_bracket(self):
        return self in {
            TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACKET, TokenType.RBRACKET,
            TokenType.LBRACE, TokenType.RBRACE
        }

    @property
    def is_structural(self):
        return self in {
            TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACKET, TokenType.RBRACKET,
            TokenType.LBRACE, TokenType.RBRACE,
            TokenType.COMMA, TokenType.COLON,
            TokenType.NEWLINE, TokenType.INDENT
        }


class Token:

    def __init__(self, token_type: TokenType = TokenType.UNKNOWN, value: str = "", pos: PositionRange = PositionRange()) -> None:

        self.token_type: TokenType = token_type
        self.value: str = value
        self.position: PositionRange = pos

    def add_to_value(self, value: str) -> None:
        self.value += value
        self.position.end.translate(1)

    def remove_from_value(self, amount: int) -> str:
        result = self.value[-amount:]
        self.value = self.value[:-amount]
        self.position.end.translate(-1)
        return result

