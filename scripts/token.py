from enum import IntEnum

from position import PositionRange


class TokenType(IntEnum):
    UNKNOWN = -1
    INDENT = 0
    NEW_LINE = 1
    KEYWORD_LINE_END = 2
    KEYWORD = 3
    OPERATION = 4
    ARGUMENT = 5
    FUNCTION = 6
    COMMENT = 7
    VALUE = 8

    @property
    def is_indent_next(self) -> bool:
        return self in {TokenType.INDENT, TokenType.NEW_LINE}

class Token:

    def __init__(self, token_type: TokenType = TokenType.UNKNOWN, value: str = "", pos: PositionRange = PositionRange()) -> None:

        self.token_type: TokenType = token_type
        self.value: str = value
        self.int_value: int = 0
        self.position: PositionRange = pos

    def add_to_value(self, value: str) -> None:
        self.value += value
        self.position.end.translate(1)
    def remove_from_value(self, amount: int) -> str:
        result = self.value[-amount:]
        self.value = self.value[:-amount]
        self.position.end.translate(-1)
        return result

