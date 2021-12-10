from __future__ import annotations

import numpy as np

from .Tools import Shape


class GridMap:
    size = (20, 20)
    data_type = np.dtype([("tile_type", np.int_), ("texture", np.int_)])
    default = 0

    def __init__(self):
        self.map = np.full(self.size, self.default, dtype=self.data_type)


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
