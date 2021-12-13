from __future__ import annotations

from .Tools import lock
from .map import Position, Map, GridMap


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

    def __setattr__(self, key, value):
        if key in self.required_stats:
            self.stats[key] = value
        else:
            raise ValueError(f"stat {key} doesn't exist")

    def __getitem__(self, item):
        return self.stats[item]

    def __setitem__(self, key, value):
        if key in self.required_stats:
            self.stats[key] = value
        else:
            raise ValueError(f"stat {key} doesn't exist")


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
        pass


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
    def __init__(self, world: World, pos: Position, stats: EntityStats, status: Status):
        """
        Entity class
        :param pos: position
        :param stats: statistics of entity (not changing often, for example damage power, name)
        :param status: status of entity (changing often, fot example health, action)
        """
        self.world = world
        self.pos = pos
        self.stats = stats
        self.status = status
        self.status.connect(self)

    def move(self, by_x: int, by_y: int):
        self.pos.move(by_x, by_y)
        self.pos.clip_in(GridMap.size)


class World:
    def __init__(self, board: Map):
        self.board = board
        self.entities: set[Entity] = set()
