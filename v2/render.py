from game2dboard import Board


class Render():
    IMAGES = {"#": "wall", ".": "pellet", "o": "power", "-": "door"}

    def __init__(self, maze):
        self.maze = maze
        self.rows = maze.rows
        self.cols = maze.cols

        self.board = Board(self.rows, self.cols)
        self.board.cell_size = 30
        self.board.cell_color = "black"

    def draw(self):
        """Full redraw: maze first, then ghosts, then Pac-Man on top."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c] = self.IMAGES.get(self.maze.grid[r][c])

        for ghost in self.maze.ghosts:
            r, c = ghost.pos
            self.board[r][c] = ghost.image

        r, c = self.maze.pacman.pos
        self.board[r][c] = "pacman"

    def draw_cell(self, pos):
        """Redraw one cell: Pac-Man or a ghost if present, else the maze tile."""
        r, c = pos
        if pos == self.maze.pacman.pos:
            self.board[r][c] = "pacman"
            return
        for ghost in self.maze.ghosts:
            if ghost.pos == pos:
                self.board[r][c] = ghost.image
                return
        self.board[r][c] = self.IMAGES.get(self.maze.grid[r][c])

    def set_title(self, text):
        self.board.title = text

    def show(self):
        self.board.show()       # Blocks until the window closes, so call it last