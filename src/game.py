from constants import MAZE, DIRS, TICK_MS, FRIGHTENED_TICKS
from maze import Maze
from render import Render
from pathfinding import bfs
import random


class Game():
    def __init__(self, maze, render):
        self.maze = maze
        self.render = render
        self.pacman = maze.pacman
        self.ghosts = maze.ghosts
        self.score = 0
        self.ticks = 0
        self.frightened_ticks = 0

        render.board.on_key_press = self.on_key
        render.board.on_timer = self.tick

    def next_pos(self, pos, d):
        dr, dc = DIRS[d]
        pr, pc = pos
        return (pr +dr, (pc+dc) % self.maze.cols)

    def can_move(self, d):
        return self.next_pos(self.pacman.pos, d) in self.maze.pacman_graph[self.pacman.pos]

    def on_key(self, key):
        if key in DIRS:
            self.pacman.next_direction = key


    def eat(self):
        r, c = self.pacman.pos
        if self.maze.grid[r][c] == ".":
            self.score += 10
            self.maze.grid[r][c] = " "
            self.maze.pellets_left -= 1
        elif self.maze.grid[r][c] == "o":
            self.score += 50
            self.maze.grid[r][c] = " "
            self.maze.pellets_left -= 1
            self.frighten()
        self.update_title()

    def update_title(self):
        self.render.set_title(f"Score: {self.score} Lives: {self.pacman.lives}")

    def frighten(self):
        self.frightened_ticks = FRIGHTENED_TICKS
        for ghost in self.ghosts:
            ghost.frightened = True
            self.render.draw_cell(ghost.pos)

    def update_frightened(self):
        if self.frightened_ticks > 0:
            self.frightened_ticks -= 1
            if self.frightened_ticks == 0:
                for ghost in self.ghosts:
                    ghost.frightened = False
                    self.render.draw_cell(ghost.pos)

    def occupied(self, pos):
        for ghost in self.ghosts:
            if ghost.pos == pos:
                return True
        return False

    def check_collision(self, ghost):
        if ghost.pos != self.pacman.pos:
            return False
        if ghost.frightened:
            ghost.reset()
            ghost.frightened = False
            ghost.prev = None
            self.score += 200
            self.render.draw_cell(ghost.pos)
            self.update_title()
            return False
        self.lose_life()
        return True

    def lose_life(self):
        self.pacman.lives -= 1

        if self.pacman.lives == 0:
            self.render.board.stop_timer()
            self.render.set_title(f"Game Over! Score: {self.score}")
            return

        self.ticks = 0
        self.frightened_ticks = 0
        self.pacman.reset()
        self.pacman.direction = None
        self.pacman.next_direction = None
        for ghost in self.ghosts:
            ghost.reset()
            ghost.frightened = False
            ghost.prev = None
        self.render.draw()
        self.update_title()

    def pacman_move(self):
        p = self.pacman
        if p.next_direction and self.can_move(p.next_direction):
            p.direction = p.next_direction
        if p.direction and self.can_move(p.direction):
            old = p.pos
            p.pos = self.next_pos(old, p.direction)
            self.eat()
            self.render.draw_cell(old)
            self.render.draw_cell(p.pos)
            for ghost in self.ghosts:
                if self.check_collision(ghost):
                    return True
        return False

    def ghost_move(self, ghost):
        old = ghost.pos
        if ghost.frightened:
            new = self.random_step(ghost)
        else:
            new = bfs(self.maze.ghost_graph, old, self.pacman.pos)
        if self.occupied(new):
            return False
        ghost.prev = old
        ghost.pos = new
        self.render.draw_cell(old)
        self.render.draw_cell(new)
        return self.check_collision(ghost)

    def random_step(self, ghost):
        options = self.maze.ghost_graph[ghost.pos]
        forward = []
        for cell in options:
            if cell != ghost.prev:
                forward.append(cell)
        if forward:
            return random.choice(forward)
        return random.choice(options)

    def tick(self):
        self.ticks += 1

        if self.pacman_move():
            return

        if self.maze.pellets_left == 0:
            self.render.board.stop_timer()
            self.render.set_title(f"You win! Score: {self.score}")
            return

        self.update_frightened()

        if self.ticks % 2 == 0:
            if self.ticks > 40:
                released = [self.ghosts[1], self.ghosts[0], self.ghosts[2]]
            elif self.ticks > 20:
                released = [self.ghosts[1], self.ghosts[0]]
            elif self.ticks > 2:
                released = [self.ghosts[1]]
            else:
                released = []

            for ghost in released:
                if self.ghost_move(ghost):
                    return


    def run(self):
        self.render.draw()
        self.update_title()
        self.render.board.start_timer(TICK_MS)
        self.render.show()

if __name__ == "__main__":
    maze = Maze(MAZE)
    if maze.valid:
        Game(maze, Render(maze)).run()
    else:
        print("The maze is not solvable: Pac-Man can't reach every pellet.")
