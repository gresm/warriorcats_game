"""
Editor for sprite sheets
"""
from __future__ import annotations

import sys
import importlib.util
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

if not output_json.exists():
    print("Creating output file...")
    output_json.touch()

# Import custom_loaders.py
custom_loaders_path = Path(__file__).parent.parent.parent / "game" / "custom_loaders.py"
custom_loaders_spec = importlib.util.spec_from_file_location("custom_loaders", str(custom_loaders_path))
custom_loaders = importlib.util.module_from_spec(custom_loaders_spec)
custom_loaders_spec.loader.exec_module(custom_loaders)
SpriteSheet = custom_loaders.SpriteSheet

# Load the image
image = pg.image.load(str(editing_image))

# Create a window of image size
pg.init()
window = pg.display.set_mode(image.get_size())
center = pg.Vector2(image.get_width() // 2, image.get_height() // 2)
sprite_sheet = SpriteSheet(image.copy())

# Mainloop variables
running = True
fps = 60
clock = pg.time.Clock()


# Define extra variables
real_selection: pg.Rect | None = None
cached_selection: pg.Rect | None = None
start_pressing = pg.Vector2()
cached_image = image.copy()
image_offset = pg.Vector2(0, 0)
zoom = 1
zoom_down_speed = 0.9
zoom_up_speed = 1/zoom_down_speed


# Define some constants
RIGHT = pg.Vector2(1, 0)
DOWN = pg.Vector2(0, 1)


# Define some functions
def point_on_image(point: pg.Vector2 | tuple) -> pg.Vector2:
    """
    Get the point position on the image, taking into account the zoom and the image offset
    """
    if isinstance(point, tuple):
        point = pg.Vector2(point) - center
    return (point - image_offset) / zoom


def get_mouse_on_image() -> pg.Vector2:
    """
    Get the mouse position on the image, taking into account the zoom and the image offset
    """
    return point_on_image(pg.mouse.get_pos())


# Mainloop
while running:
    # Set some variables before the loop
    reload_cached_image = False
    reload_cached_selection = False
    reload_all = False
    mouse_pressed = pg.mouse.get_pressed()
    mouse_pos = get_mouse_on_image()
    keys_pressed = pg.key.get_pressed()
    cached_image_rect = cached_image.get_rect().copy()
    image_offset.x = int(image_offset.x)
    image_offset.y = int(image_offset.y)

    # Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_BACKQUOTE:
                # Reset zoom and image offset
                zoom = 1
                image_offset = pg.Vector2(0, 0)
                reload_all = True
            elif event.key == pg.K_SPACE:
                # Add selection to the sprite sheet
                if real_selection is not None:
                    pg.display.quit()
                    name = input("Name of the element: ")
                    sprite_sheet.add_element(name, tuple(real_selection))
                    real_selection = None
                    reload_all = True

                    pg.display.init()
                    window = pg.display.set_mode(image.get_size())
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Left click
                start_pressing = pg.Vector2(mouse_pos)
                # If we have a current selection, we are removing it
                if real_selection:
                    real_selection = None
                    reload_cached_selection = True
            elif event.button == 2:
                # Middle click
                pass
            elif event.button == 3:
                # Right click
                pass

    # Define some variables after the events loop
    if cached_selection:
        cached_selection_center = pg.Vector2(cached_selection.center)
    else:
        cached_selection_center = None

    # Handle currently pressed mouse/keyboard keys

    if mouse_pressed[0]:
        # Left click
        if real_selection is None:
            real_selection = pg.Rect(start_pressing, pg.Vector2(0, 0))
        else:
            real_selection = pg.Rect(start_pressing, mouse_pos - start_pressing)
        reload_cached_selection = True

    # Selection manipulation

    # Check if selection exists
    if real_selection:
        if keys_pressed[pg.K_LEFT]:
            real_selection.size -= RIGHT
            reload_cached_selection = True
        if keys_pressed[pg.K_RIGHT]:
            real_selection.size += RIGHT
            reload_cached_selection = True
        if keys_pressed[pg.K_UP]:
            real_selection.size -= DOWN
            reload_cached_selection = True
        if keys_pressed[pg.K_DOWN]:
            real_selection.size += DOWN
            reload_cached_selection = True
        if keys_pressed[pg.K_w]:
            real_selection.topleft -= DOWN
            reload_cached_selection = True
        if keys_pressed[pg.K_s]:
            real_selection.topleft += DOWN
            reload_cached_selection = True
        if keys_pressed[pg.K_a]:
            real_selection.topleft -= RIGHT
            reload_cached_selection = True
        if keys_pressed[pg.K_d]:
            real_selection.topleft += RIGHT
            reload_cached_selection = True
        if keys_pressed[pg.K_i]:
            real_selection.size += DOWN
            real_selection.topleft -= DOWN
            reload_cached_selection = True
        if keys_pressed[pg.K_k]:
            real_selection.size -= DOWN
            real_selection.topleft += DOWN
            reload_cached_selection = True
        if keys_pressed[pg.K_j]:
            real_selection.size += RIGHT
            real_selection.topleft -= RIGHT
            reload_cached_selection = True
        if keys_pressed[pg.K_l]:
            real_selection.size -= RIGHT
            real_selection.topleft += RIGHT
            reload_cached_selection = True
        if keys_pressed[pg.K_DELETE] or keys_pressed[pg.K_BACKSPACE]:
            real_selection = None
            reload_cached_selection = True

    # Zoom
    if keys_pressed[pg.K_EQUALS]:
        zoom *= zoom_up_speed
        reload_all = True
    if keys_pressed[pg.K_MINUS]:
        zoom *= zoom_down_speed
        reload_all = True
    if keys_pressed[pg.K_0]:
        zoom = 1
        reload_all = True

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
        reload_all = True
    if keys_pressed[pg.K_y]:
        zoom *= zoom_down_speed
        reload_all = True

    # Keep zoom above 0
    if zoom == 0:
        zoom = 0.00001

    if reload_all:
        reload_cached_image = True
        reload_cached_selection = True

    # Reload cached image if needed
    if reload_cached_image:
        # Reload image
        cached_image = pg.transform.scale(image, (int(image.get_width() * zoom), int(image.get_height() * zoom)))

    # Reload cached selection if needed
    if reload_cached_selection:
        # Check if selection exists
        if real_selection:
            # Copy selection
            cached_selection = real_selection.copy()

            # Rescale cached selection
            cached_selection.size = (int(cached_selection.size[0] * zoom), int(cached_selection.size[1] * zoom))

            # Reposition cached selection relatively to cached image
            cached_selection.topleft = pg.Vector2(real_selection.topleft) * zoom

        else:
            # Set cached selection to None
            cached_selection = None

    # Clear window
    window.fill((0, 0, 0))

    # Draw the image
    image_blit_rect = cached_image.get_rect()
    image_blit_rect.center = center + image_offset
    window.blit(cached_image, image_blit_rect)

    if cached_selection:
        selection_blit_rect = cached_selection.copy()
        selection_blit_rect.center = pg.Vector2(selection_blit_rect.center) + center + image_offset
        pg.draw.rect(window, (255, 0, 0), selection_blit_rect, 1)

    # Update the display
    pg.display.update()

    # Update the clock
    clock.tick(fps)


# Close the window
pg.quit()

# Save the sprite sheet
raw = json.dumps(sprite_sheet.config)
output_json.write_text(raw)
