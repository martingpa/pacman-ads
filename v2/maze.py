from constants import MAZE, GHOSTS
from entities import PacMan, Ghost

class Maze():
    def __init__(self, maze):
        self.grid = [list(string) for string in maze]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.ghosts = []
        self.pacman = None

        self.parse()
        self.pacman_graph = self.build_graph(False)
        self.ghost_graph = self.build_graph(True)

    def parse(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == "G":
                    self.grid[i][j] = " "
                    name = GHOSTS[len(self.ghosts)]
                    self.ghosts.append(Ghost((i,j), name))
                elif self.grid[i][j] == "P":
                    self.grid[i][j] = " "
                    self.pacman = PacMan((i, j))

    def neighbors(self, pos, ghost):

        blocked = "#" if ghost else "#-"

        result = []
        directions = [(1,0), (-1, 0), (0, 1), (0, -1)]

        pr = pos[0]
        pc = pos[1]

        for dr, dc in directions:                           # dr (direction row), dc (direction collumn)
            if self.grid[pr+dr][(pc+dc) % self.cols] not in blocked:
                result.append((pr+dr, (pc+dc) % self.cols))

        return result


    def build_graph(self, ghost):
        graph = {}

        blocked = "#" if ghost else "#-"

        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] not in blocked:
                    graph[(i,j)] = []

        for key in graph:
            graph[key].extend(self.neighbors(key, ghost))

        return graph
