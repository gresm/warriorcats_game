from __future__ import annotations


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


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


class Status:
    def __init__(self, info):
        self.effects: Effects = Effects()
        self.action = None
        self.info = info
        self.object: Entity | None = None

    def connect(self, entity: Entity):
        self.object = entity
        self.effects.connect(entity)


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
