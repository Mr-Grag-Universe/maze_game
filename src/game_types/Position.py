from dataclasses import dataclass

@dataclass
class Position:
    x : int
    y : int

    def __add__(self, val):
        if isinstance(val, tuple):
            return Position(self.x + val[0], self.y + val[1])
        if isinstance(val, dict):
            return Position(self.x + val['x'], self.y + val['y'])
        else:
            return Position(self.x + val.x, self.y + val.y)

    def __eq__(self, val) -> bool:
        if isinstance(val, tuple):
            return self.x == val[0] and self.y == val[1]
        if isinstance(val, dict):
            return self.x == val['x'] and self.y == val['y']
        else:
            return self.x == val.x and self.y == val.y

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)