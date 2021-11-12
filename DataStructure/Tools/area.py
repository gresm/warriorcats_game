from __future__ import annotations

from typing import Sequence

from . import Position


class Rect:
    def __init__(self, pos: Position, size: Position):
        self.pos = pos
        self.size = size

    def in_range(self, pos: Position):
        return self.pos.x < pos.x < self.pos.x + self.size.x and self.pos.y < pos.y < self.pos.y + self.size.y

    def out_range(self, pos: Position):
        return (self.pos.x > pos.x or pos.x > self.pos.x + self.size.x) and \
               (self.pos.y > pos.y or pos.y > self.pos.y + self.size.y)

    def on_border(self, pos: Position):
        return not (self.in_range(pos) or self.out_range(pos))


class Shape:
    def __init__(self, rect: Rect | Shape, *r: Rect | Shape, exclude: Sequence[Rect | Shape] = ()):
        self.rects: list[Rect | Shape] = [rect] + list(r)
        self.exclude: list[Rect | Shape] = list(exclude)

    def in_range(self, pos: Position) -> bool:
        mach = False
        for r in self.rects:
            if r.in_range(pos):
                mach = True
                break

        if mach:
            for e in self.exclude:
                if e.in_range(pos):
                    return False
            return True
        return False

    def out_range(self, pos: Position) -> bool:
        mach = False
        for r in self.rects:
            if r.out_range(pos):
                mach = True
                break

        if mach:
            for e in self.exclude:
                if e.out_range(pos):
                    return False
            return True
        return False

    def on_border(self, pos: Position) -> bool:
        mach = False
        for r in self.rects:
            if r.on_border(pos):
                mach = True
                break

        if mach:
            for e in self.exclude:
                if e.on_border(pos):
                    return False
            return True
        return False


__all__ = [
    "Rect",
    "Shape"
]
