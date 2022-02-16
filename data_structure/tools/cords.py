from __future__ import annotations

from typing import overload, Sequence, Iterable


class Cords(list):
    x: float
    y: float

    @overload
    def __init__(self, xy: Sequence[float, float]):
        ...

    @overload
    def __init__(self, x: float, y: float):
        ...

    @overload
    def __init__(self, pos: "Cords"):
        ...

    @overload
    def __init__(self, iterable: Iterable[float]):
        ...

    def __init__(self, *args, **kwargs):
        x = None
        y = None

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
            elif isinstance(args[0], Cords):
                x, y = args[0].xy
            elif hasattr(args[0], "__iter__") or hasattr(args[0], "__list__"):
                lst = list(args[0])
                if len(lst) != 2:
                    raise TypeError("iterable yielded incorrect amount of data")

                for el in lst:
                    if not isinstance(el, (float, int)):
                        raise TypeError(f"iterable yielded {el}, expected float")
            else:
                raise TypeError(f"incorrect data, got {args[0]}")
        else:
            raise TypeError(f"expected at most 2 argument, got {len(args)}")

        if "pos" in kwargs:
            x, y = kwargs["pos"].xy
        elif "xy" in kwargs:
            x, y = kwargs["xy"]
        elif "iterable" in kwargs:
            lst = list(kwargs["iterable"])
            if len(lst) != 2:
                raise TypeError("iterable yielded incorrect amount of data")

            for el in lst:
                if not isinstance(el, (float, int)):
                    raise TypeError(f"iterable yielded {el}, expected float")

        if "x" in kwargs:
            x = kwargs["x"]

        if "y" in kwargs:
            y = kwargs["y"]

        if x is None or y is None:
            raise TypeError("x or y are not specified")

        if not isinstance(x, (int, float)):
            raise TypeError(f"expected float, got {x}")

        if not isinstance(y, (int, float)):
            raise TypeError(f"expected float, got {y}")

        super().__init__((x, y))

    def __add__(self, other: Cords | float) -> Cords:
        if isinstance(other, Cords):
            return self.new(self.x + other.x, self.y + other.y)
        return self.new(self.x + other, self.y + other)

    def __sub__(self, other: Cords | float) -> Cords:
        if isinstance(other, Cords):
            return self.new(self.x - other.x, self.y - other.y)
        return self.new(self.x - other, self.y - other)

    def __truediv__(self, other: Cords | float) -> Cords:
        if isinstance(other, Cords):
            return self.new(self.x / other.x, self.y / other.y)
        return self.new(self.x / other, self.y / other)

    def __floordiv__(self, other: Cords | float) -> Cords:
        if isinstance(other, Cords):
            return self.new(self.x // other.x, self.y // other.y)
        return self.new(self.x // other, self.y // other)

    def __mul__(self, other: Cords | float):
        """
        Not valid mathematical implementation...
        :param other:
        :return:
        """
        if isinstance(other, Cords):
            return self.new(self.x * other.x, self.y * other.y)
        return self.new(self.x * other, self.y * other)

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self is other or (isinstance(other, Cords) and self.x == other.x and self.y == other.y)

    @classmethod
    def new(cls, x: float, y: float) -> Cords:
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

    def dot(self, other: Cords) -> float:
        return self.x * other.x + self.y * other.y

    def move(self, x: float = 0, y: float = 0):
        return self.__class__(self.x + x, self.y + y)

    def move_ip(self, x: float = 0, y: float = 0):
        self.x += x
        self.y += y

    def goto(self, x: float, y: float):
        self.x = x
        self.y = y

    def copy(self):
        return self.move()

    def cord(self):
        return int(self.x), int(self.y)
