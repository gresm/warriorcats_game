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
