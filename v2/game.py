from constants import MAZE, DIRS, TICK_MS, FRIGHTENED_TICKS
from maze import Maze
from render import Render
from pathfinding import bfs, dijkstra
import random


class Game():
    def __init__(self, maze, render):
        self.maze = maze
        self.render = render
        self.pacman = maze.pacman
        self.ghosts = maze.ghosts
        self.score = 0
        self.ticks = 0
        self.frightened_ticks = 0       # > 0 while a power pellet is active

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
        pos = self.pacman.pos
        if pos in self.maze.pellets:
            self.score += 10
            self.maze.pellets.remove(pos)
        elif pos in self.maze.power_pellets:
            self.score += 50
            self.maze.power_pellets.remove(pos)
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
        # count down the power pellet, ghosts go back to normal when it ends
        if self.frightened_ticks > 0:
            self.frightened_ticks -= 1
            if self.frightened_ticks == 0:
                for ghost in self.ghosts:
                    ghost.frightened = False
                    self.render.draw_cell(ghost.pos)
    
    def check_collision(self, ghost):
        # returns True if Pac-Man died
        if ghost.pos != self.pacman.pos:
            return False
        if ghost.frightened:
            ghost.reset()               # back to the ghost house
            self.score += 200
            self.render.draw_cell(ghost.pos)
            self.update_title()
            return False
        self.lose_life()
        return True
    
    def lose_life(self):
        self.pacman.lives -= 1

        # no lives left: game over, don't start a new life
        if self.pacman.lives == 0:
            self.render.board.stop_timer()
            self.render.set_title(f"Game Over! Score: {self.score}")
            return

        # start a new life: everyone back to their start cells
        self.ticks = 0
        self.frightened_ticks = 0
        self.pacman.reset()             # also clears direction and next_direction
        for ghost in self.ghosts:
            ghost.reset()               # also clears frightened
        self.render.draw()
        self.update_title()
    
    def pacman_move(self):
        # returns True if Pac-Man died
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

    def ghost_move(self, ghost, distances):
        # returns True if Pac-Man died
        old = ghost.pos
        if ghost.frightened:
            # frightened: a random neighbor
            new = self.random_step(ghost)
        elif ghost.name == "blinky":
            # Blinky: shortest path to Pac-Man with BFS (every step costs the same)
            new = bfs(self.maze.ghost_graph, old, self.pacman.pos)
        else:
            # Pinky and Inky: step to the neighbor with the smallest Dijkstra distance to Pac-Man
            new = self.closest_neighbor(old, distances)
        ghost.prev = old
        ghost.pos = new
        self.render.draw_cell(old)
        self.render.draw_cell(new)
        return self.check_collision(ghost)

    def closest_neighbor(self, pos, distances):
        neighbors = self.maze.ghost_graph[pos]
        best = neighbors[0]
        for neighbor in neighbors:
            if distances[neighbor] < distances[best]:
                best = neighbor
        return best

    def random_step(self, ghost):
        # random neighbor, but not straight back if there is another way
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

        # 1. Pac-Man
        if self.pacman_move():
            return

        # 2. Win when every pellet is eaten
        if len(self.maze.pellets) == 0 and len(self.maze.power_pellets) == 0:
            self.render.board.stop_timer()
            self.render.set_title(f"You win! Score: {self.score}")
            return

        # 3. Power pellet countdown
        self.update_frightened()

        # 4. Ghosts move every second tick. ghosts[1] (Blinky) is the middle one, right below the door,
        #    so he is released first
        if self.ticks % 2 == 0:
            if self.ticks > 40:
                released = [self.ghosts[1], self.ghosts[0], self.ghosts[2]]
            elif self.ticks > 20:
                released = [self.ghosts[1], self.ghosts[0]]
            elif self.ticks > 2:
                released = [self.ghosts[1]]
            else:
                released = []

            # one Dijkstra run from Pac-Man per tick, shared by Pinky and Inky
            distances = dijkstra(self.maze.build_weighted_graph(), self.pacman.pos)
            for ghost in released:
                if self.ghost_move(ghost, distances):
                    return      # Pac-Man died: stop so the others don't move off their reset positions


    def run(self):
        self.render.draw()
        self.update_title()
        self.render.board.start_timer(TICK_MS)
        self.render.show()

if __name__ == "__main__":
    maze = Maze(MAZE)
    Game(maze, Render(maze)).run()