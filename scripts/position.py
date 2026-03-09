class PositionRange:
    def __init__(self, x1: int = 0, y1: int = 0, x2: int = 0, y2: int = 0) -> None:
        self.start: Position = Position(x1, y1)
        self.end: Position = Position(x2, y2)

class Position:

    def __init__(self, x: int = 0, y: int = 0) -> None:

        self.x: int = x
        self.y: int = y

    def translate(self, x: int = 0, y: int = 0) -> None:
        self.x += x
        self.y += y
