import pygame as pg

from game import scene_manager as scenes
from game import size, game
from game.scenes import MainMenuScene

scenes.spawn_scene(MainMenuScene)


@game.frame
def frame(window, delta_time):
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            game.stop()
        else:
            scenes.handle_events(ev)

    scenes.update()

    window.fill((0, 0, 0))

    scenes.draw(window)

    pg.display.update()


if __name__ == '__main__':
    game.run()
