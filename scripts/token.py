from enum import IntEnum

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
        return self in {TokenType.UNKNOWN, TokenType.INDENT, TokenType.NEW_LINE}

class Token:

    def __init__(self, token_type: TokenType = TokenType.UNKNOWN, value: str = "", pos: tuple[tuple[int, int], tuple[int, int]] = ((0, 0), (0, 0))) -> None:

        self.token_type: TokenType = token_type
        self.value: str = value
        self.int_value: int = 0
        self.position: tuple[tuple[int, int], tuple[int, int]] = pos

    def add_to_value(self, value: str) -> None:
        self.value += value
        self.position = self.position[0], (self.position[1][0] + 1, self.position[1][1])

    def translate_start_pos(self, x: int, y: int) -> None:
        self.position = (self.position[0][0] + x, self.position[0][1] + y), self.position[1]

    def translate_end_pos(self, x: int, y: int) -> None:
        self.position = self.position[0], (self.position[1][0] + x, self.position[1][1] + y)
