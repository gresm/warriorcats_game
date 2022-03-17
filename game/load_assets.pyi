import pygame as _pg

from data_structure import Map as _Map

from . import SpriteSheet as __SpriteSheet

class __Menu:
    background: _pg.Surface
    lobby_background: _pg.Surface
    play_rect: _pg.Rect
    quit_rect: _pg.Rect
    continue_button: _pg.Surface


class __Game:
    entry_map: _Map


menu = __Menu
game = __Game
font: _pg.font.Font
sprite_sheet: __SpriteSheet

__all__ = [
    "menu",
    "game",
    "font"
]

del _Map
