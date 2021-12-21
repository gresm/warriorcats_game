import pygame as pg

size = (800, 800)
window = pg.display.set_mode(size)

running = True

while running:
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running = False

    window.fill((0, 0, 0))

    pg.display.update()
