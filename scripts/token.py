from enum import Enum, auto


class TokenType(Enum):
    VALUE = auto()
    EQUAL = auto()
    OPERATOR = auto()
    EQUAL_OPERATOR = auto()
    STRING = auto()
    NUMBER = auto()
    COMMENT = auto()

    QUESTION = auto()
    EXCLAMAITON = auto()
    DOT = auto()
    COMMA = auto()
    COLON = auto()

    INDENT = auto()
    NEWLINE = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    EOF = auto()


    @property
    def is_bracket(self) -> bool:
        return self in {
            TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACKET, TokenType.RBRACKET,
            TokenType.LBRACE, TokenType.RBRACE
        }

    @property
    def is_structural(self) -> bool:
        return self in {
            TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACKET, TokenType.RBRACKET,
            TokenType.LBRACE, TokenType.RBRACE,
            TokenType.COMMA, TokenType.COLON,
            TokenType.NEWLINE, TokenType.INDENT
        }


class Token:

    def __init__(self, token_type: TokenType, value: str | int = "") -> None:
        self.token_type: TokenType = token_type
        self.value: str | int = value

    def __repr__(self) -> str:
        return f"{self.token_type.name}: {self.value}"

