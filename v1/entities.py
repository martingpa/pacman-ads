"""Moving entities."""

import random

from constants import DIRS
from pathfinding import bfs_next_step


class Ghost:
    def __init__(self, name, pos):
        self.name = name        # Also the image name
        self.pos = pos          # (row, col)
        self.start = pos        # Spawn cell, for resets
        self.prev = None        # Previous cell, so random moves avoid reversing
        self.frightened = False

    @property
    def image(self):
        return "frightened" if self.frightened else self.name

    def reset(self):
        self.pos = self.start
        self.prev = None
        self.frightened = False

    def target(self, game):
        """Cell this ghost aims for."""
        pr, pc = game.pacman_pos
        dr, dc = DIRS[game.direction] if game.direction else (0, 0)
        if self.name == "pinky":                    # 4 cells ahead of Pac-Man
            return game.clamp((pr + 4 * dr, pc + 4 * dc))
        if self.name == "inky":                     # Blinky -> 2 ahead of Pac-Man, doubled
            br, bc = game.ghost("blinky").pos
            ar, ac = pr + 2 * dr, pc + 2 * dc
            return game.clamp((2 * ar - br, 2 * ac - bc))
        return game.pacman_pos                      # Blinky: Pac-Man himself

    def random_step(self, game):
        """Random neighbor, avoiding going straight back if possible."""
        options = game.neighbors(self.pos)
        forward = [cell for cell in options if cell != self.prev]
        return random.choice(forward or options)

    def move(self, game):
        old = self.pos
        if self.frightened:
            step = self.random_step(game)
        else:
            step = bfs_next_step(self.pos, self.target(game), game.neighbors)
            if step == self.pos:                    # Already at target: wander
                step = self.random_step(game)
        self.prev, self.pos = old, step
