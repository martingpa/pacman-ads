from constants import GHOSTS
from entities import PacMan, Ghost

class Maze():
    def __init__(self, maze):
        self.grid = [list(string) for string in maze]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.ghosts = []
        self.pacman = None
        self.pellets = set()          # positions of the "." pellets
        self.power_pellets = set()    # positions of the "o" power pellets

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
                elif self.grid[i][j] == ".":
                    self.grid[i][j] = " "
                    self.pellets.add((i, j))
                elif self.grid[i][j] == "o":
                    self.grid[i][j] = " "
                    self.power_pellets.add((i, j))

    def neighbors(self, pos, ghost):

        if ghost:
            blocked = "#"           # ghosts can go through the door
        else:
            blocked = "#-"          # Pac-Man can't

        result = []
        directions = [(1,0), (-1, 0), (0, 1), (0, -1)]

        pr = pos[0]
        pc = pos[1]

        for dr, dc in directions:                           # dr (direction row), dc (direction collumn)
            if self.grid[pr+dr][(pc+dc) % self.cols] not in blocked:
                result.append((pr+dr, (pc+dc) % self.cols))

        return result


    def build_graph(self, ghost):
        # create the graph dictionary (adjacency list)
        graph = {}

        if ghost:
            blocked = "#"
        else:
            blocked = "#-"

        # add every cell we can walk on as a key with an empty list
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] not in blocked:
                    graph[(i,j)] = []

        # fill each list with the cell's walkable neighbors
        for key in graph:
            graph[key].extend(self.neighbors(key, ghost))

        # return the graph
        return graph
