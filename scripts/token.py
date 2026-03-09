from enum import Enum

class TokenType(Enum):
    INDENT = 0
    KEYWORD = 1
    OPERATION = 2
    ARGUMENT = 3
    FUNCTION = 4
    KEYWORD_LINE_END = 5
    NEW_LINE = 6

class Token:

    def __init__(self, token_type: TokenType, value: str = "", pos: tuple[tuple[int, int], tuple[int, int]] = ((0, 0), (0, 0))) -> None:

        self.token_type: TokenType = token_type
        self.value: str = value
        self.position: tuple[tuple[int, int], tuple[int, int]] = pos

    def add_to_value(self, x: str) -> None:
        self.value += x
        self.position = self.position[0], (self.position[1][0] + 1, self.position[1][1])

    def translate_start_pos(self, x: int, y: int) -> None:
        self.position = (self.position[0][0] + x, self.position[0][1] + y), self.position[1]

    def translate_end_pos(self, x: int, y: int) -> None:
        self.position = self.position[0], (self.position[1][0] + x, self.position[1][1] + y)
