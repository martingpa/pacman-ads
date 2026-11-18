from constants import MAZE, DIRS, TICK_MS
from maze import Maze
from render import Render
from pathfinding import bfs
import random


class Game():
    def __init__(self, maze, render, auto = False):
        self.maze = maze
        self.render = render
        self.pacman = maze.pacman
        self.ghosts = maze.ghosts
        self.score = 0
        self.ticks = 0
        self.auto = auto

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
        elif self.maze.grid[r][c] == "o":
            self.score += 50
            self.maze.grid[r][c] = " "
        self.render.set_title(f"Score: {self.score} Lives: {self.pacman.lives}")
    
    def occupied(self, pos):
        for ghost in self.ghosts: 
            if ghost.pos == pos:
                return True
    
    def check_collision(self, ghost):
        if ghost.pos != self.pacman.pos:
            return 
        if ghost.frightened:
            ghost.reset()
            self.score += 200
        else:
            self.lose_life()
    
    def lose_life(self):
        self.pacman.lives -= 1
        self.ticks = 0
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
        self.render.draw()
        if self.pacman.lives <= 0:
            self.render.board.stop_timer()
            self.render.set_title("Game Over!")
    
    def pacman_move(self):
        p = self.pacman
        if self.auto == False:
            if p.next_direction and self.can_move(p.next_direction):
                p.direction = p.next_direction
            if p.direction and self.can_move(p.direction):
                old = p.pos
                p.pos = self.next_pos(old, p.direction)
                self.eat()
                for ghost in self.ghosts:
                    self.check_collision(ghost)
                self.render.draw_cell(old)
                self.render.draw_cell(p.pos)
        elif self.auto == True:
            graph = self.maze.build_weighted_graph()

            old = p.pos
            options = graph[old]          

            safe = []
            for neighbor, weight in options:
                if weight >= 3:
                    safe.append(neighbor)
            if safe:
                new = random.choice(safe)
            else:
                new, best_weight = options[0]
                for neighbor, weight in options:
                    if weight > best_weight:
                        new, best_weight = neighbor, weight

            p.pos = new
            self.eat()
            for ghost in self.ghosts:
                self.check_collision(ghost)
            self.render.draw_cell(old)
            self.render.draw_cell(p.pos)            
                       

    def ghost_move(self, ghost):
        gp = ghost.pos
        pp = self.pacman.pos
        graph = self.maze.ghost_graph 

        old = gp
        new = bfs(graph, gp, pp)  
        if self.occupied(new):
            return
        ghost.pos = new
        self.check_collision(ghost)
        self.render.draw_cell(old)
        self.render.draw_cell(ghost.pos)
        
    
    def tick(self):
        self.ticks += 1
        
        self.pacman_move()
        
        if self.ticks % 2 == 0: 
            if self.ticks > 40:
                for ghost in self.ghosts:
                    self.ghost_move(ghost)
            elif self.ticks > 20 and (self.ticks % 2 == 0):
                self.ghost_move(self.ghosts[0])
                self.ghost_move(self.ghosts[1])
            elif self.ticks > 2 and (self.ticks % 2 == 0):
                self.ghost_move(self.ghosts[0])


    def run(self):
        self.render.draw()
        self.render.board.start_timer(TICK_MS)
        self.render.show()

if __name__ == "__main__":
    from render import Render
    maze = Maze(MAZE)
    Game(maze, Render(maze), auto = False).run()