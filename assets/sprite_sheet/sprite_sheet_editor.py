"""
Editor for sprite sheets
"""

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
                pass
            elif event.button == 2:
                # Middle click
                pass
            elif event.button == 3:
                # Right click
                pass

    # Draw the image
    window.blit(image, (0, 0))
    pg.display.update()

    # Update the clock
    clock.tick(fps)
