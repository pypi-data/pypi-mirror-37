from functools import reduce
from typing import List, Optional

from vis2048.vec2 import Vec2


class MutSqMat:
    """
    A square mutable matrix that can be flipped and rotated.
    """

    def __init__(self, width: int, _items=None):
        self.width = width
        self._items = _items or [None for _ in range(width * width)]

    def rotate(self, right_angles: int):
        """
        Rotates the matrix by the given amount of right angles counter-clockwise.
        """
        right_angles %= 4

        if right_angles == 0:
            return

        old = self.copy()
        for x in range(self.width):
            for y in range(self.width):
                self[Vec2(x, y)] = old[Vec2(self.width - 1 - y, x)]

        self.rotate(right_angles - 1)

    def flip_vertical(self):
        """
        Flip along the vertical axis.
        """
        old = self.copy()

        for x in range(self.width):
            for y in range(self.width):
                self[Vec2(x, y)] = old[Vec2(self.width - x - 1, y)]

    def copy(self):
        return MutSqMat(self.width, self._items.copy())

    def set_row(self, idx: int, row: List[Optional[int]]):
        start = idx * self.width
        end = start + self.width
        self._items[start:end] = row

    def get_row(self, idx: int) -> List[Optional[int]]:
        start = idx * self.width
        end = start + self.width
        return self._items[start:end]

    def __contains__(self, item):
        return item in self._items

    def __eq__(self, other):
        if not isinstance(other, MutSqMat):
            raise TypeError()
        return self._items == other._items

    def __hash__(self):
        return reduce(lambda l, r: l ^ r, [hash(str(x)) for x in self._items])

    def __getitem__(self, coord) -> Optional[int]:
        if not isinstance(coord, Vec2):
            raise TypeError()
        return self._items[coord.x + coord.y * self.width]

    def __setitem__(self, coord, value):
        if not isinstance(coord, Vec2):
            raise TypeError()
        self._items[coord.x + coord.y * self.width] = value
