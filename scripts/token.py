from enum import Enum

class TokenType(Enum):
    INDENT = 0
    KEYWORD = 1
    OPERATION = 2
    ARGUMENT = 3
    FUNCTION = 4
    KEYWORD_LINE_END = 5

class Token:

    def __init__(self, token_type: TokenType, value: str, pos: tuple[tuple[int, int], tuple[int, int]]) -> None:

        self.token_type = token_type
        self.value = value
        self.position = pos
