from __future__ import annotations

from .entities import Position


class Area:
    def __init__(self, pos: Position, size: Position):
        self.pos = pos
        self.size = size


class Map:
    def __init__(self, *areas: Area):
        pass
