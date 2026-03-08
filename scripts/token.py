class Token:

    def __init__(self, token_type: str, value: str, pos: tuple[tuple[int, int], tuple[int, int]]) -> None:

        self.token_type = token_type
        self.value = value
        self.position = pos
