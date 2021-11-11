from __future__ import annotations

from typing import overload, Sequence


class Position(list):
    x: float
    y: float

    @overload
    def __init__(self, xy: Sequence[float, float]):
        ...

    @overload
    def __init__(self, x: float, y: float):
        ...

    @overload
    def __init__(self, pos: "Position"):
        ...

    def __init__(self, *args, **kwargs):
        x = None
        y = None

        if "pos" in kwargs:
            x, y = kwargs["pos"].xy
        elif "xy" in kwargs:
            x, y = kwargs["xy"]

        if "x" in kwargs:
            x = kwargs["x"]

        if "y" in kwargs:
            y = kwargs["y"]

        if len(args) == 2:
            x, y = args
        elif len(args) == 1:
            if isinstance(args[0], tuple):
                if len(args[0]) == 2:
                    if isinstance(args[0][0], (float, int)) and isinstance(args[0][1], (float, int)):
                        x, y = args[0]
                    else:
                        tps = []
                        for el in args[0]:
                            tps.append(type(el))
                        raise TypeError(f"expected (float, float) got {tuple(tps)}")
                else:
                    tps = []
                    for el in args[0]:
                        tps.append(type(el))
                    raise TypeError(f"expected (float, float) got {tuple(tps)}")
            elif isinstance(args[0], Position):
                x, y = args[0].xy
        else:
            raise TypeError(f"expected at most 2 argument, got {len(args)}")

        if x is None or y is None:
            raise TypeError("x or y are not specified")

        if not isinstance(x, (int, float)):
            raise TypeError(f"expected float, got {type(x)}")

        if not isinstance(y, (int, float)):
            raise TypeError(f"expected float, got {type(y)}")

        super().__init__((x, y))

    def __add__(self, other: Position | float) -> Position:
        if isinstance(other, Position):
            return self.new(self.x + other.x, self.y + other.y)
        return self.new(self.x + other, self.y + other)

    def __sub__(self, other: Position | float) -> Position:
        if isinstance(other, Position):
            return self.new(self.x - other.x, self.y - other.y)
        return self.new(self.x - other, self.y - other)

    def __truediv__(self, other: Position | float) -> Position:
        if isinstance(other, Position):
            return self.new(self.x / other.x, self.y / other.y)
        return self.new(self.x / other, self.y / other)

    def __floordiv__(self, other: Position | float) -> Position:
        if isinstance(other, Position):
            return self.new(self.x // other.x, self.y // other.y)
        return self.new(self.x // other, self.y // other)

    def __mul__(self, other: Position | float):
        """
        Not valid mathematical implementation...
        :param other:
        :return:
        """
        if isinstance(other, Position):
            return self.new(self.x * other.x, self.y * other.y)
        return self.new(self.x * other, self.y * other)

    @classmethod
    def new(cls, x: float, y: float) -> Position:
        return cls(x, y)

    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, value: float):
        self[0] = value

    @property
    def y(self) -> float:
        return self[1]

    @y.setter
    def y(self, value: float):
        self[1] = value

    @property
    def xy(self):
        return self.x, self.y

    @property
    def xx(self):
        return self.x, self.x

    @property
    def yy(self):
        return self.y, self.y

    @property
    def yx(self):
        return self.y, self.x

    def dot(self, other: Position) -> float:
        return self.x * other.x + self.y * other.y

    def move(self, x: float = 0, y: float = 0):
        return self.__class__(self.x + x, self.y + y)

    def copy(self):
        return self.move()
