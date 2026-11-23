from constants import GHOSTS
from entities import PacMan, Ghost

class Maze():
    def __init__(self, maze):
        self.grid = [list(string) for string in maze]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.ghosts = []
        self.pacman = None
        self.pellets_left = 0         # pellets and power pellets still in the grid

        # check with DFS that Pac-Man can reach every pellet before setting up the game
        self.valid = self.is_solvable()
        if self.valid:
            self.parse()
            self.pacman_graph = self.build_graph(False)
            self.ghost_graph = self.build_graph(True)

    def is_solvable(self):
        # find Pac-Man's start
        start = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == "P":
                    start = (i, j)
        if start is None:
            return False

        # visit every cell Pac-Man can reach
        visited = set()
        self.dfs(start, visited)

        # every pellet and power pellet must have been visited
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == "." or self.grid[i][j] == "o":
                    if (i, j) not in visited:
                        return False
        return True

    def dfs(self, pos, visited):
        # depth-first search (recursion): visit pos, then each neighbor we haven't visited yet
        visited.add(pos)
        for neighbor in self.neighbors(pos, False):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

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
                elif self.grid[i][j] == "." or self.grid[i][j] == "o":
                    self.pellets_left += 1      # pellets stay in the grid, we only count them

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
