# Algorithms and Data Structures – Group Project: Pac-Man

## 1. Object-Oriented Structure

The program is structured in 6 classes and one function, distributed across 5 files in the **src** folder:

- `Entity` in **entities.py**
    - `PacMan` (inherits from `Entity`) in **entities.py**
    - `Ghost` (inherits from `Entity`) in **entities.py**
- `Maze` in **maze.py**
- `Game` in **game.py**
- `Render` in **render.py**
- the function `bfs()` in **pathfinding.py**

An additional **constants.py** file also exists.

### 1.1. Entities

There are two entity types within the game:

- PacMan
- The Ghosts

Each is represented by its own class, `PacMan` and `Ghost`, and both inherit from the `Entity` class.

- `Entity` has four attributes: the current position `pos`, the start position `start`, the current direction `direction` and the direction buffer `next_direction`. Its one method, `reset()`, sets the current position back to the start position.

    > **Note:** The direction buffer lets the game check that a direction is valid before the entity actually takes it.

    - `Ghost` adds its identifier `name`, its state `frightened` and its previous cell `prev`, so a frightened ghost doesn't turn straight back.
    - `PacMan` adds a `lives` counter.
    - Both have an `image()` method that returns the image to draw.

### 1.2. Maze

`Maze` is the core class in terms of algorithms and data structures.

**Attributes**

- `grid` stores the maze (initially defined as an array of strings) as a matrix.
- `pacman_graph` maps each traversable cell to the adjacent cells PacMan can move to.
- `ghost_graph` is the same, except that ghosts can also traverse `-`, which is why a separate graph is needed.
- `pellets_left` counts the pellets still in the grid.

**Methods**

- **`is_solvable()`** runs first. It finds PacMan in the grid and uses `dfs()` to visit every cell he can reach. If a pellet wasn't visited the maze is not valid, and `parse()` and `build_graph()` are not run.
- **`dfs()`** is a recursive depth-first search over the grid.
- **`parse()`** loops through the `MAZE` defined in constants and:
    - finds each ghost, creates a `Ghost` object with its name and position, and appends it to `ghosts`. The `G` symbol is replaced with an empty space `" "`.
    - finds PacMan, creates a `PacMan` object with its position, and replaces `P` with `" "`.
    - counts the pellets.
- **`neighbors()`** takes a position in the grid and checks which adjacent positions an entity can traverse. Ghosts can traverse everything except `#`, PacMan everything except `#` and `-`.
- **`build_graph()`** builds the adjacency map from the grid: each traversable cell is a key, and its value is the list of its neighbors.

### 1.3. Pathfinding

`bfs()` returns the first step an entity should take towards a target, as a position and not a direction. It uses a `deque` as the queue and a `parent` dictionary that is also the visited set. The ghosts use it to follow PacMan.

### 1.4. Game

**Functional Logic**

- **`on_key()`** handles key presses. If the key is a valid direction, it sets the `next_direction` of PacMan.
- **`tick()`** runs every `TICK_MS` milliseconds: it moves PacMan, checks the win, counts down the power pellet and, every second tick, moves the ghosts. The ghosts leave the house one by one (after tick 2, 20 and 40).

**Game Logic**

- **`pacman_move()`** changes direction if `next_direction` is valid, moves PacMan, eats and checks for collisions.
- **`ghost_move()`** moves a ghost one step towards PacMan with `bfs()`, or to a random neighbor if it is frightened. If another ghost is in the way (`occupied()`) it waits.
- **`eat()`** adds 10 points for a pellet and 50 for a power pellet, which also calls `frighten()`.
- **`frighten()`** makes the ghosts frightened for 40 ticks. A frightened ghost can be eaten for 200 points.
- **`check_collision()`** checks whether a ghost and PacMan are on the same cell, in which case it calls `lose_life()`.
- **`lose_life()`** subtracts 1 from the `lives` counter and resets the entities. When PacMan runs out of lives, it stops the timer and displays `"Game Over!"`.
- **`next_pos()`** and **`can_move()`** work out the next cell in a direction (wrapping around at the tunnels) and whether PacMan can go there.

### 1.5. Render

`Render` handles displaying the game. `draw()` draws the whole board and `draw_cell()` updates a single cell, which is faster than redrawing everything. Images are stored in the **img** folder.

### 1.6. Data structures

- 2D array (list of lists) for the grid
- dictionaries for the graphs and the BFS parents
- `deque` as the BFS queue
- set for the cells visited by DFS
- counter for the pellets left

### 1.7. What we abandoned

An autoplayer. It ran a BFS for every neighbor of every cell every tick, so it was slow, and it couldn't win. We also tried Dijkstra and our own queue and heap, but went back to BFS and `deque` to keep it simple.

## 2. Running the Code

This requires Python 3.10 or newer. With [uv](https://docs.astral.sh/uv/), from the repository root, run:

```
uv run python src/game.py
```

Or install the library and run the file:

```
pip install game2dboard==0.8
python src/game.py
```

Control PacMan with the arrow keys.
