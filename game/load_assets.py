import pygame as pg
import pygame_assets as assets


class _Menu:
    background = assets.load.image("menu_background.png")
    play_rect = pg.Rect(90, 550, 300, 100)
    quit_rect = pg.Rect(420, 550, 300, 100)


menu = _Menu
