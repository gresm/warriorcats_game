import pygame as pg

from game import scene_manager
from game.scenes import MainMenuScene


size = (800, 800)
window = pg.display.set_mode(size)
running = True

scene_manager.spawn_scene(MainMenuScene)


while running:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False
        else:
            scene_manager.handle_events(ev)

    scene_manager.update()

    window.fill((0, 0, 0))

    scene_manager.draw(window)

    pg.display.update()
