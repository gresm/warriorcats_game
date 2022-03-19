"""
Custom loaders for pygame-assets
Probably will be removed in the future, as pygame-assets is unmaintained
"""

from __future__ import annotations

from pathlib import Path
import json
import pygame as pg
from pygame_assets import load
from pygame_assets.loaders import loader


class SpriteSheet:
    def __init__(
            self, image: pg.Surface, config: dict[str, tuple[int, int, int, int] | tuple[int, int, int, int, int, int]]
    ):
        self.config = config
        self.image = image
        self.elements: dict[str, pg.Surface | IndexedSpriteSheet] = {}
        self.error_image = load.image("missing.png")

    def get_element(self, name: str, is_indexed: bool = False, auto: bool = False) -> pg.Surface | IndexedSpriteSheet:
        # Check if element exists in config, if not, return error image
        if name not in self.config:
            return self.error_image

        # Check if element has already been loaded, if not, load it
        if name not in self.elements:
            # Check if element is a single image
            if len(self.config[name]) == 4:
                self.elements[name] = self.image.subsurface(self.config[name])
            else:
                # Check if element is a sprite sheet
                self.elements[name] = IndexedSpriteSheet(
                    self.image.subsurface(self.config[name][:4]), self.config[name][4:]
                )
            self.elements[name] = self.image.subsurface(self.config[name])

        # Return element, if indexed, return indexed sprite sheet, if not, return surface
        # Unless auto is True, in which case return the automatically loaded element

        if auto:
            return self.elements[name]

        if is_indexed:
            ret = self.elements[name]
            if isinstance(ret, IndexedSpriteSheet):
                return ret
            return IndexedSpriteSheet(ret, ret.get_size())

        ret = self.elements[name]
        if isinstance(ret, IndexedSpriteSheet):
            return ret.image
        return ret


class IndexedSpriteSheet:
    def __init__(self, image: pg.Surface, tile_size: tuple[int, int]):
        self.image = image
        self.tile_size = tile_size
        self.elements: list[pg.Surface] = []
        self.error_image = load.image("missing.png")

        # Create list of elements
        for i in range(0, self.image.get_width(), self.tile_size[0]):
            for j in range(0, self.image.get_height(), self.tile_size[1]):
                self.elements.append(self.image.subsurface((i, j, self.tile_size[0], self.tile_size[1])))

    def get_element(self, index: int) -> pg.Surface:
        # Check if element index is in range, if not, return error image scaled to tile size
        if index < 0 or index >= len(self.elements):
            return pg.transform.scale(self.error_image, self.tile_size)

        return self.elements[index]


@loader("sprite_sheet")
def sprite_sheet(filepath, config: dict[str, tuple[int, int, int, int]] | str):
    """
    Loads a sprite sheet from a filepath
    """
    # load config from file, if it is a string
    if isinstance(config, str):
        with Path(config).open() as f:
            config = json.load(f)

    path = Path(filepath)
    print(filepath)
    return SpriteSheet(load.image(str(path)), config)


__all__ = [
    "sprite_sheet",
    "SpriteSheet"
]
