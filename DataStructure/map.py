from __future__ import annotations

import numpy as np

from .Tools import Shape, Cords


class GridMap:
    size = (20, 20)
    data_type = np.dtype([("tile_type", np.int_), ("texture", np.int_)])
    default = 0

    def __init__(self):
        self.map = np.full(self.size, self.default, dtype=self.data_type)

    def in_range(self, pos: tuple[int, int]):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]


class MapChunk:
    def __init__(self, triggers: dict[str, Shape], grid: GridMap):
        self.triggers = triggers
        self.grid = grid


class Map:
    def __init__(self, tile: MapChunk, extra_tiles: dict[tuple[int, int], MapChunk] | None = None):
        self.tiles: dict[tuple[int, int], MapChunk] = {(0, 0): tile}
        extra_tiles = extra_tiles if extra_tiles else {}
        extra_copy = extra_tiles.copy()
        extra_copy.update(self.tiles)
        self.tiles = extra_copy


class Position:
    # noinspection PyShadowingBuiltins
    def __init__(self, map: Map, chunk: tuple[int, int], exact: tuple[int, int]):
        self.map = map
        self.chunk = Cords(chunk)
        self.local = Cords(exact)

    @property
    def area(self):
        return self.chunk.cord()

    @area.setter
    def area(self, value: tuple[int, int]):
        self.chunk.goto(*value)

    @property
    def exact(self):
        return self.local.cord()

    @exact.setter
    def exact(self, value: tuple[int, int]):
        self.local.goto(*value)

    def exists(self) -> bool:
        return self.chunk in self.map.tiles and self.map.tiles[self.area].grid.in_range(self.exact)
