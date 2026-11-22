from game2dboard import Board


class Render():
    IMAGES = {"#": "wall", "-": "door"}

    def __init__(self, maze):
        self.maze = maze
        self.rows = maze.rows
        self.cols = maze.cols

        self.board = Board(self.rows, self.cols)
        self.board.cell_size = 30
        self.board.cell_color = "black"

    def draw(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.draw_cell((r, c))

    def draw_cell(self, pos):
        r, c = pos
        if pos == self.maze.pacman.pos:
            self.board[r][c] = self.maze.pacman.image()
            return
        for ghost in self.maze.ghosts:
            if ghost.pos == pos:
                self.board[r][c] = ghost.image()
                return
        if pos in self.maze.pellets:
            self.board[r][c] = "pellet"
        elif pos in self.maze.power_pellets:
            self.board[r][c] = "power"
        else:
            self.board[r][c] = self.IMAGES.get(self.maze.grid[r][c])

    def set_title(self, text):
        self.board.title = text

    def show(self):
        self.board.show()       # Blocks until the window closes, so call it last