import random
from typing import Optional, List

from vis2048.mat import MutSqMat
from vis2048.vec2 import Vec2


class Game:
    """
    Square game grid with maximum and minimum tile values and tracked score.
    """

    def __init__(self, width: int, min_tile: int, max_tile: int):
        self.score = 0

        self.min_tile = min_tile
        self.max_tile = max_tile

        self.mat = MutSqMat(width)

    @property
    def width(self) -> int:
        return self.mat.width

    def left(self) -> bool:
        changed = False

        for y in range(self.width):
            row = self.mat.get_row(y)
            old = row.copy()
            self._move_left(row)
            self.mat.set_row(y, row)

            if old != row:
                changed = True

        return changed

    def right(self) -> bool:
        self.mat.flip_vertical()
        changed = self.left()
        self.mat.flip_vertical()

        return changed

    def up(self) -> bool:
        self.mat.rotate(1)
        changed = self.left()
        self.mat.rotate(3)

        return changed

    def down(self) -> bool:
        self.mat.rotate(3)
        changed = self.left()
        self.mat.rotate(1)

        return changed

    def stuck(self) -> bool:
        """
        Determines whether the game is stuck (i.e. no action can be performed).
        """
        if None in self.mat:
            return False

        for x in range(self.width):
            for y in range(self.width):
                value = self.mat[Vec2(x, y)]

                # Does any tile have an adjacent tile with the same value?
                if 0 < x and value == self.mat[Vec2(x - 1, y)] \
                        or 0 < y and value == self.mat[Vec2(x, y - 1)] \
                        or x < self.width - 1 and value == self.mat[Vec2(x + 1, y)] \
                        or y < self.width - 1 and value == self.mat[Vec2(x, y + 1)]:
                    return False

        return True

    def won(self) -> bool:
        """
        Determines whether the game has been won by producing the largest tile.
        """
        return self.max_tile in self.mat

    def full(self) -> bool:
        """
        Determines whether the game grid is full of tiles.
        """
        return None not in self.mat

    def place_two(self):
        """
        Place a 2-valued tile in a random location.
        :raises ValueError When the grid is in a full state
        """
        if self.full():
            raise ValueError('Cannot place tile since game grid is full')

        empty_indices = []
        for i, v in enumerate(self.mat._items):
            if v is None:
                empty_indices.append(i)

        choice = random.choice(empty_indices)

        self.mat._items[choice] = 2

    def _move_left(self, line: List[Optional[int]]):
        """
        Processes a line of tiles using the rules defined by the game.
        """
        for curr_idx, current_value in enumerate(line):
            # Iterate through all following indices
            for follow_idx in range(curr_idx + 1, len(line)):
                follow_value = line[follow_idx]

                if follow_value is not None:
                    if current_value is None:
                        current_value = follow_value
                        line[curr_idx] = follow_value
                        line[follow_idx] = None
                        continue

                    # Merge when values are the same
                    if follow_value == current_value:
                        current_value *= 2
                        self.score += current_value
                        line[curr_idx] = current_value
                        line[follow_idx] = None
                        break

                    # Shift non-mergeable
                    else:
                        line[follow_idx] = None
                        line[curr_idx + 1] = follow_value
                        break
