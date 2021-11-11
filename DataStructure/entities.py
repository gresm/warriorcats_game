from __future__ import annotations

from typing import overload, Sequence

from .Tools import lock


class Position(list):
    x: float
    y: float

    @overload
    def __init__(self, xy: Sequence[float, float]): ...

    @overload
    def __init__(self, x: float, y: float): ...

    @overload
    def __init__(self, pos: "Position"): ...
    
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


class Stats:
    required_stats: set[str] = set()

    def __init__(self, stats: dict[str, ...]):
        for name in self.required_stats:
            if name not in stats:
                raise ValueError(f"'{name}' is not given in setup")

        self.stats = stats

    def __dir__(self):
        val = tuple(super().__dir__())
        val += tuple(self.required_stats)
        return val

    def __getattr__(self, item):
        return self.stats[item]


class Effect:
    def __init__(self, lasting_time: int):
        self.lasting_time = lasting_time
        self.object: Entity | None = None

    def connect(self, entity: Entity):
        self.object = entity

    def stop(self):
        self.object.status.effects.remove(self)

    def tick(self):
        if self.lasting_time < 0:
            self.stop()
        else:
            self.act()
            self.lasting_time -= 1

    def act(self):
        """
        Override me to change effect behaviour
        :return:
        """


class Effects:
    def __init__(self, *effects: Effect):
        self.effects: set[Effect] = set() if len(effects) == 0 else set(effects)
        self.object: Entity | None = None

    def connect(self, entity: Entity):
        self.object = entity

        for effect in self.effects:
            effect.connect(entity)

    def add(self, effect: Effect):
        self.effects.add(effect)
        effect.connect(self.object)

    def remove(self, effect: Effect):
        if effect in self.effects:
            self.effects.remove(effect)

    def clear(self):
        self.effects.clear()

    def tick(self):
        for effect in self.effects:
            effect.tick()


class Action:
    _actions: dict[int, Action]
    _current_id = 0

    def __init__(self, name: str):
        self.name = name
        self.id = self._current_id
        self._current_id += 1

        self._actions[self.id] = self

    def __eq__(self, other):
        return other is self or self.id == other or self.name == other

    @classmethod
    def get_from_id(cls, action_id: int):
        return cls._actions[action_id] if action_id in cls._actions else None

    @classmethod
    def get(cls, name: str):
        for el in cls._actions:
            if cls._actions[el].name == name:
                return cls._actions[el]
        return None


NoAction = Action("NoAction")


class Info:
    def __init__(self):
        self.damage: int = 0

        self.object: Entity | None = None

    @lock
    def connect(self, entity: Entity):
        self.object = entity

    @property
    @connect.locked
    def health(self):
        return self.object.stats["max_health"]

    @health.setter
    @connect.locked
    def health(self, value):
        self.damage = self.health - value


class Status:
    def __init__(self, info: Info):
        self.effects: Effects = Effects()
        self.action: Action = NoAction
        self.info = info
        self.object: Entity | None = None

    @lock
    def connect(self, entity: Entity):
        self.object = entity
        self.effects.connect(entity)
        self.info.connect(entity)


class EntityStats(Stats):
    required_stats = {"damage_power", "speed", "max_health"}


class Entity:
    def __init__(self, pos: Position, stats: EntityStats, status: Status):
        """
        Entity class
        :param pos: position
        :param stats: statistics of entity (not changing often, for example damage power, name)
        :param status: status of entity (changing often, fot example health, action)
        """
        self.pos = pos

        self.stats = stats

        self.status = status
        self.status.connect(self)
