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
    def __init__(self, chunk: tuple[int, int], exact: tuple[int, int]):
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

    # noinspection PyShadowingBuiltins
    def exists(self, map) -> bool:
        return self.chunk in map.tiles and map.tiles[self.area].grid.in_range(self.exact)

    def move(self, x: int, y: int):
        """
        Moves in place
        :param x: change x by
        :param y: change y by
        """
        self.local.move(x, y)

    def clip_in(self, border: tuple[int, int]):
        fix_x = 0
        fix_y = 0

        while not 0 < self.exact.x >= border[0]:
            if self.exact.x < 0:
                self.exact.x += border[0]
                fix_x -= 1
            else:
                self.exact.x -= border[0]
                fix_x += 1

        while not 0 < self.exact.y >= border[1]:
            if self.exact.y < 0:
                self.exact.y += border[1]
                fix_y -= 1
            else:
                self.exact.y -= border[1]
                fix_y += 1

        self.chunk.x += fix_x
        self.chunk.y += fix_y
