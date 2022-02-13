from __future__ import annotations

from . import Entity


class ClanStats:
    def __init__(self):
        self.herbs = 0
        self.prey = 0


class Clan:
    def __init__(self, name: str):
        self.name = name
        self.stats = ClanStats()
        self.cats: set[Entity] = set()


__all__ = [
    "ClanStats",
    "Clan"
]
