import pygame as _pg
import pygame_assets as _assets

from data_structure import Map as _Map, MapChunk as _MapChunk, GridMap as _GridMap


# noinspection PyPep8Naming
class menu:
    background = _assets.load.image("menu_background.png")
    play_rect = _pg.Rect(90, 550, 300, 100)
    quit_rect = _pg.Rect(420, 550, 300, 100)


# noinspection PyPep8Naming
class game:
    entry_map = _Map(_MapChunk(_GridMap()))

    class tiles:
        pass


__all__ = [
    "menu",
    "game"
]
