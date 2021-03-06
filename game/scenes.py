from __future__ import annotations

import pygame as pg

from . import BaseScene, game, assets
import data_structure as ds


# PLAY X, Y = 90, 550
# QUIT X, Y = 420, 550
# SIZE X, Y = 300, 100

class MainMenuScene(BaseScene):
    def update(self):
        for ev in self.get_events():
            if ev.type == pg.MOUSEBUTTONUP:
                if assets.menu.play_rect.collidepoint(*ev.pos):
                    self.manager.spawn_scene(LobbyScene)
                elif assets.menu.quit_rect.collidepoint(*ev.pos):
                    game.stop()

    def draw(self, surface: pg.Surface):
        surface.blit(assets.menu.background, (0, 0))


class LobbyScene(BaseScene):
    player_names: set[str] = set()
    player_names_list: list[str] = []
    typing_text: str
    text_max_with: int = 200
    text_height: int = 35
    offset = 20, 20
    right_buffer = 20
    names_spacing = 20
    typing_rect_border = pg.Vector2(10, 0)
    name_min_length = 3

    next_button_rect: pg.Rect

    def init(self, *args, **kwargs):
        self.player_names = set()
        self.typing_text = ""
        self.next_button_rect = pg.Rect(0, 0, 0, 0)

    def update(self):
        for ev in self.get_events():
            if ev.type == pg.KEYDOWN:
                if ev.unicode:
                    if ev.unicode == "\r":
                        if len(self.typing_text) < self.name_min_length or self.typing_text in self.player_names:
                            continue
                        self.player_names.add(self.typing_text)
                        self.player_names_list.append(self.typing_text)
                        self.typing_text = ""
                        continue
                    elif ev.unicode == "\b":
                        self.typing_text = self.typing_text[:-1]
                        continue
                    self.typing_text += ev.unicode
                    if assets.font.size(self.typing_text)[0] > self.text_max_with:
                        self.typing_text = self.typing_text[:-1]
            elif ev.type == pg.MOUSEBUTTONUP:
                # if there are at least 2 players and the next button is clicked
                if len(self.player_names) > 1 and self.next_button_rect.collidepoint(*ev.pos):
                    self.manager.spawn_scene(GameScene)

    def draw(self, surface: pg.Surface):
        surface.blit(assets.menu.lobby_background, (0, 0))
        rend = assets.font.render(self.typing_text, False, "white")
        surface.blit(rend, pg.Vector2(surface.get_rect().center) - rend.get_rect().center)

        current_draw = pg.Vector2(self.offset)
        for name in self.player_names_list:
            rend = assets.font.render(name, False, "white")
            new_pos = pg.Vector2(current_draw)
            new_pos.x += rend.get_width() + self.names_spacing

            if new_pos.x > surface.get_width() - self.right_buffer:
                new_pos.x = self.offset[0] + rend.get_width() + self.names_spacing
                new_pos.y += self.text_height
                current_draw.x = self.offset[0]
                current_draw.y += self.text_height

            surface.blit(rend, current_draw)
            boundary = pg.Vector2(5, 5)
            rect = pg.Rect(current_draw - boundary, pg.Vector2(rend.get_size()) + boundary * 2)
            pg.draw.rect(surface, "white", rect, 1)
            current_draw = new_pos

        # draw the centered text box
        rect = pg.Rect(
            surface.get_rect().center - pg.Vector2(
                self.text_max_with // 2, self.text_height // 2
            ) - self.typing_rect_border,
            pg.Vector2(self.text_max_with, self.text_height) + self.typing_rect_border * 2
        )

        pg.draw.rect(surface, "white", rect, 1)

        # draw "continue" button if there are at least 2 players
        if len(self.player_names) >= 2:
            self.next_button_rect = surface.blit(
                assets.menu.continue_button,
                (
                    surface.get_width() - assets.menu.continue_button.get_width(),
                    surface.get_height() - assets.menu.continue_button.get_height()
                )
            )


class GameScene(BaseScene):
    game: ds.Game

    def init(self, *args, **kwargs):
        # create game using player names and game map from assets
        self.game = ds.Game(assets.game.entry_map, *LobbyScene.player_names_list)

    def update(self):
        pass

    def draw(self, surface: pg.Surface):
        pass

    def draw_chunk(self, surface: pg.Surface, chunk_x: int, chunk_y: int):
        # get the chunk from the game world map using the chunk coordinates
        chunk = self.game.world.board.tiles[(chunk_x, chunk_y)]
        grid = chunk.grid
        # iterate over tiles in the chunk
        for line in grid.map:
            for tile in line:
                pass
