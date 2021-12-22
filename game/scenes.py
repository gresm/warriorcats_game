from __future__ import annotations

import pygame as pg
import pygame_assets as assets

from . import BaseScene
from . import game


menu_background = assets.load.image("menu_background.png")


# PLAY X, Y = 90, 550
# QUIT X, Y = 420, 550
# SIZE X, Y = 300, 100

class MainMenuScene(BaseScene):
    play_rect: pg.Rect
    quit_rect: pg.Rect

    def init(self, *args, **kwargs):
        self.play_rect = pg.Rect(90, 550, 300, 100)
        self.quit_rect = pg.Rect(420, 550, 300, 100)

    def update(self):
        for ev in self.get_events():
            if ev.type == pg.MOUSEBUTTONUP:
                if self.play_rect.collidepoint(*ev.pos):
                    self.manager.spawn_scene(PlayScene)
                elif self.quit_rect.collidepoint(*ev.pos):
                    game.stop()

    def draw(self, surface: pg.Surface):
        surface.blit(menu_background, (0, 0))


class PlayScene(BaseScene):
    pass
