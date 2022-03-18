"""
Editor for sprite sheets
"""
from __future__ import annotations

import sys
import json

import pygame as pg

from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python3 sprite_sheet_editor.py <sprite_sheet_image> <sprite_sheet_json>")
    print("Please provide a sprite sheet image and a sprite sheet json file.")
    editing_image = Path(input("Sprite sheet image: "))
    output_json = Path(input("Sprite sheet json: "))
elif len(sys.argv) == 2:
    print("Usage: python3 sprite_sheet_editor.py <sprite_sheet_image> <sprite_sheet_json>")
    print("Please provide a  sprite sheet json file.")
    editing_image = sys.argv[1]
    output_json = Path(input("Sprite sheet json: "))
else:
    editing_image = Path(sys.argv[1])
    output_json = Path(sys.argv[2])

assert editing_image.exists()

# Load the image
image = pg.image.load(str(editing_image))

# Create a window of image size
pg.init()
window = pg.display.set_mode(image.get_size())

# Mainloop variables
running = True
fps = 60
clock = pg.time.Clock()


# Define extra variables
current_selection: pg.Rect | None = None
start_pressing = pg.Vector2(0, 0)
image_offset = pg.Vector2(0, 0)
zoom = 1
zoom_down_speed = 0.9
zoom_up_speed = 1/zoom_down_speed
cached_image = image.copy()


# Define some constants
RIGHT = pg.Vector2(1, 0)
DOWN = pg.Vector2(0, 1)


# Mainloop
while running:
    # Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Left click
                start_pressing = pg.Vector2(event.pos)
                # If we have a current selection, we are removing it
                if current_selection:
                    current_selection = None
            elif event.button == 2:
                # Middle click
                pass
            elif event.button == 3:
                # Right click
                pass

    # Read currently pressed mouse keys
    mouse_pressed = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    if mouse_pressed[0]:
        # Left click
        if current_selection is None:
            current_selection = pg.Rect(start_pressing, pg.Vector2(0, 0))
        else:
            current_selection.size = pg.Vector2(mouse_pos) - start_pressing

    # Read currently pressed keys
    keys_pressed = pg.key.get_pressed()

    # Selection manipulation

    if keys_pressed[pg.K_LEFT]:
        current_selection.size -= RIGHT
    if keys_pressed[pg.K_RIGHT]:
        current_selection.size += RIGHT
    if keys_pressed[pg.K_UP]:
        current_selection.size -= DOWN
    if keys_pressed[pg.K_DOWN]:
        current_selection.size += DOWN
    if keys_pressed[pg.K_w]:
        current_selection.topleft -= DOWN
    if keys_pressed[pg.K_s]:
        current_selection.topleft += DOWN
    if keys_pressed[pg.K_a]:
        current_selection.topleft -= RIGHT
    if keys_pressed[pg.K_d]:
        current_selection.topleft += RIGHT
    if keys_pressed[pg.K_i]:
        current_selection.size += DOWN
        current_selection.topleft -= DOWN
    if keys_pressed[pg.K_k]:
        current_selection.size -= DOWN
        current_selection.topleft += DOWN
    if keys_pressed[pg.K_j]:
        current_selection.size += RIGHT
        current_selection.topleft -= RIGHT
    if keys_pressed[pg.K_l]:
        current_selection.size -= RIGHT
        current_selection.topleft += RIGHT
    if keys_pressed[pg.K_DELETE]:
        current_selection = None
    if keys_pressed[pg.K_BACKSPACE]:
        current_selection = None

    reload_cached_image = False

    # Zoom
    if keys_pressed[pg.K_EQUALS]:
        zoom *= zoom_up_speed
        reload_cached_image = True
    if keys_pressed[pg.K_MINUS]:
        zoom *= zoom_down_speed
        reload_cached_image = True
    if keys_pressed[pg.K_0]:
        zoom = 1
        reload_cached_image = True

    # Update image offset with t, g, f, h
    if keys_pressed[pg.K_t]:
        image_offset -= DOWN
    if keys_pressed[pg.K_g]:
        image_offset += DOWN
    if keys_pressed[pg.K_f]:
        image_offset -= RIGHT
    if keys_pressed[pg.K_h]:
        image_offset += RIGHT

    # Additional zoom keys with r, y
    if keys_pressed[pg.K_r]:
        zoom *= zoom_up_speed
        reload_cached_image = True
    if keys_pressed[pg.K_y]:
        zoom *= zoom_down_speed
        reload_cached_image = True

    # Reload cached image, if needed
    if reload_cached_image:
        if zoom == 0:
            zoom = 0.00001
        cached_image = pg.transform.scale(image, (int(image.get_width() * zoom), int(image.get_height() * zoom)))

    # Clear window
    window.fill((0, 0, 0))

    # Draw the image
    window.blit(cached_image, image_offset)
    if current_selection:
        pg.draw.rect(window, (255, 0, 0), current_selection, 1)

    # Update the display
    pg.display.update()

    # Update the clock
    clock.tick(fps)
