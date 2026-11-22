from constants import MAZE, GHOSTS, GHOST_COST
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

    def build_weighted_graph(self):
        graph = {}

        # cells with a ghost on them cost more, so Dijkstra goes around the other ghosts
        ghost_cells = set()
        for ghost in self.ghosts:
            ghost_cells.add(ghost.pos)

        for key in self.ghost_graph:
            graph[key] = []
            for neighbor in self.ghost_graph[key]:
                if neighbor in ghost_cells:
                    cost = GHOST_COST
                else:
                    cost = 1
                graph[key].append((neighbor, cost))     #(neighbor, cost of stepping onto it)

        return graph
