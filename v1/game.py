
"""Main game: state, drawing, input and the game loop. Run this file."""
 
from game2dboard import Board
 
from constants import (DIRS, FRIGHTENED_TICKS, GHOST_EVERY, GHOST_POINTS, GHOSTS,
                       IMAGES, LIVES, MAZE, PELLET_POINTS, POWER_POINTS, TICK_MS)
from entities import Ghost
 
 
class Game:
    def __init__(self, layout):
        # Game state
        self.grid = [list(row) for row in layout]  # Matrix out of the list of strings
        self.pacman_pos = None
        self.ghosts = []            # Ghost objects
        self.direction = None       # Direction Pac-Man is moving
        self.next_direction = None  # Last key pressed (buffered turn)
        self.score = 0
        self.lives = LIVES
        self.ticks = 0              # Tick counter, used for ghost speed
        self.pellets_left = 0
        self.parse()
        self.pacman_start = self.pacman_pos  # For resets after losing a life
 
        self.frightened_ticks = 0                   # > 0 while power pellet is active
 
        # Display
        self.board = Board(len(self.grid), len(self.grid[0]))
        self.board.cell_size = 30
        self.board.cell_color = "black"
        self.board.on_key_press = self.on_key
        self.board.on_timer = self.tick
 
    def parse(self):
        """Store start positions, count pellets, turn the P/G markers into floor."""
        for r, row in enumerate(self.grid):
            for c, ch in enumerate(row):
                if ch == "G":
                    name = GHOSTS[len(self.ghosts)]
                    self.ghosts.append(Ghost(name, (r, c)))   # NOTE: Initializes the position of the ghost, only runs once.
                    self.grid[r][c] = " "           # NOTE: grid should only represent the maze itself not the ghosts or PACMAN, we only store the position.
                elif ch == "P":
                    self.pacman_pos = (r, c)
                    self.grid[r][c] = " "
                elif ch in ".o":
                    self.pellets_left += 1
 
    # ---------- Helpers ----------
 
    def ghost(self, name):
        return next(g for g in self.ghosts if g.name == name)
 
    def clamp(self, pos):
        """Keep a target cell inside the board."""
        r = min(max(pos[0], 0), len(self.grid) - 1)
        c = min(max(pos[1], 0), len(self.grid[0]) - 1)
        return r, c
 
    # ---------- Drawing ----------
 
    def draw(self):
        for r, row in enumerate(self.grid):
            for c, ch in enumerate(row):
                self.board[r][c] = IMAGES.get(ch)    # NOTE: assigns each element an image.
        for ghost in self.ghosts:                    # NOTE: draws each ghost its position
            r, c = ghost.pos
            self.board[r][c] = ghost.image
        r, c = self.pacman_pos
        self.board[r][c] = "pacman"                  # NOTE: draws pacman at its position
 
    def draw_cell(self, pos):
        """Redraw one cell: Pac-Man or a ghost if one is there, else the maze tile."""
        r, c = pos
        if pos == self.pacman_pos:
            self.board[r][c] = "pacman"
            return
        for ghost in self.ghosts:
            if ghost.pos == pos:
                self.board[r][c] = ghost.image
                return
        self.board[r][c] = IMAGES.get(self.grid[r][c])
 
    def update_title(self):
        self.board.title = f"Pac-Man   Score: {self.score}   Lives: {self.lives}"
 
    # ---------- Movement ----------
 
    def on_key(self, key):
        if key in DIRS:
            self.next_direction = key
 
    def next_pos(self, pos, d):
        """Cell reached from pos moving in direction d (columns wrap for the tunnel)."""
        dr, dc = DIRS[d]
        return pos[0] + dr, (pos[1] + dc) % len(self.grid[0])
 
    def can_move(self, pos, d):
        r, c = self.next_pos(pos, d)
        return self.grid[r][c] not in "#-"  # Walls and ghost door block Pac-Man
 
    def neighbors(self, pos):
        """Walkable cells next to pos for a ghost (walls block, door doesn't)."""
        result = []
        for d in DIRS:
            r, c = self.next_pos(pos, d)
            if self.grid[r][c] != "#":
                result.append((r, c))
        return result
 
    # ---------- Game events ----------
 
    def eat(self):
        """Eat whatever is on Pac-Man's cell."""
        r, c = self.pacman_pos
        if self.grid[r][c] == ".":
            self.score += PELLET_POINTS
        elif self.grid[r][c] == "o":
            self.score += POWER_POINTS
            self.frighten()
        else:
            return
        self.grid[r][c] = " "
        self.pellets_left -= 1
 
    def frighten(self):
        self.frightened_ticks = FRIGHTENED_TICKS
        for ghost in self.ghosts:
            ghost.frightened = True
            self.draw_cell(ghost.pos)
 
    def update_frightened(self):
        """Count down Frightened mode; ghosts return to normal when it ends."""
        if self.frightened_ticks > 0:
            self.frightened_ticks -= 1
            if self.frightened_ticks == 0:
                for ghost in self.ghosts:
                    ghost.frightened = False
                    self.draw_cell(ghost.pos)
 
    def check_collisions(self):
        """Handle ghosts on Pac-Man's cell. Returns True if Pac-Man died."""
        for ghost in self.ghosts:
            if ghost.pos != self.pacman_pos:
                continue
            if ghost.frightened:                    # Pac-Man eats the ghost
                self.score += GHOST_POINTS
                ghost.reset()                       # Back to the ghost house
                self.draw_cell(ghost.pos)
                self.draw_cell(self.pacman_pos)
                self.update_title()
            else:
                self.lose_life()
                return True
        return False
 
    def lose_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.end("GAME OVER")
            return
        # Reset everyone to their start cells
        self.pacman_pos = self.pacman_start
        self.direction = None
        self.next_direction = None
        self.frightened_ticks = 0
        for ghost in self.ghosts:
            ghost.reset()
        self.draw()
        self.update_title()
 
    def end(self, message):
        self.board.stop_timer()
        self.board.title = f"{message}   Score: {self.score}"
 
    # ---------- Game loop ----------
 
    def tick(self):
        self.ticks += 1
 
        # 1. Pac-Man
        if self.next_direction and self.can_move(self.pacman_pos, self.next_direction):
            self.direction = self.next_direction
        if self.direction and self.can_move(self.pacman_pos, self.direction):
            old_pos = self.pacman_pos
            self.pacman_pos = self.next_pos(self.pacman_pos, self.direction)
            self.eat()
            self.draw_cell(old_pos)          # Only the 2 changed cells are redrawn
            self.draw_cell(self.pacman_pos)
            self.update_title()
            if self.pellets_left == 0:
                self.end("YOU WIN")
                return
 
        if self.check_collisions():          # Pac-Man walked into a ghost
            return
 
        # 2. Frightened timer
        self.update_frightened()
 
        # 3. Ghosts
        if self.ticks % GHOST_EVERY == 0:
            for ghost in self.ghosts:
                old_pos = ghost.pos
                ghost.move(self)
                self.draw_cell(old_pos)
                self.draw_cell(ghost.pos)
 
        self.check_collisions()              # A ghost walked into Pac-Man
 
    def run(self):
        self.draw()
        self.update_title()
        self.board.start_timer(TICK_MS)
        self.board.show()
 
 
if __name__ == "__main__":
    Game(MAZE).run()