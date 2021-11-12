from __future__ import annotations

from .Tools import Position, Shape


class GridMap:
    def __init__(self):
        pass


class MapTile:
    def __init__(self, triggers: dict[str, Shape]):
        self.triggers = triggers


class Map:
    def __init__(self, tile: MapTile, extra_tiles: dict[Position, MapTile] | None = None):
        self.tiles: dict[Position, MapTile] = {Position(0, 0): tile}
        extra_tiles = extra_tiles if extra_tiles else {}
        extra_copy = extra_tiles.copy()
        extra_copy.update(self.tiles)
        self.tiles = extra_copy
