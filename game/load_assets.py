import pygame as _pg
import pygame_assets as _assets

from data_structure import Map as _Map, MapChunk as _MapChunk, GridMap as _GridMap


# noinspection PyPep8Naming
class __Menu:
    background = _assets.load.image("menu_background.png")
    lobby_background = _assets.load.image("lobby_background.png")
    play_rect = _pg.Rect(90, 550, 300, 100)
    quit_rect = _pg.Rect(420, 550, 300, 100)
    continue_button = _assets.load.image("menu_continue_button.png")


# noinspection PyPep8Naming
class __Game:
    entry_map = _Map(_MapChunk(_GridMap()))

    class tiles:
        pass


menu = __Menu
game = __Game
font = _pg.font.SysFont("", 30)


__all__ = [
    "menu",
    "game",
    "font"
]
