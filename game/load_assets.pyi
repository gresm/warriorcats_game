import pygame as _pg

from data_structure import Map as _Map

class _Menu:
    background: _pg.Surface
    play_rect: _pg.Rect
    quit_rect: _pg.Rect


class _Game:
    entry_map: _Map


menu = _Menu
game = _Game
font: _pg.font.Font

__all__ = [
    "menu",
    "game",
    "font
]

del _Map
