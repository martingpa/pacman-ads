# Algorithms and Data Structures – Group Project: Pac-Man

## 1. Object-Oriented Structure

The program is structured in 8 classes and two functions, distributed across 5 files:

- `Entity` in **entities.py**
    - `PacMan` (inherits from `Entity`) in **entities.py**
    - `Ghost` (inherits from `Entity`) in **entities.py**
- `Maze` in **maze.py**
- `Game` in **game.py**
- `Render` in **render.py**
- `Node` and `QueueLinkedList` (our queue from session 13) in **pathfinding.py**
- the functions `bfs()` and `dijkstra()` in **pathfinding.py**

An additional **constants.py** file also exists.

### 1.1. Entities

There are two entity types within the game:

- PacMan
- The Ghosts

Each is represented by its own class, `PacMan` and `Ghost`, and both inherit from the `Entity` class.

- `Entity` has four attributes: the current position `pos`, the start position `start`, the current direction `direction` and the direction buffer `next_direction`. Its one method, `reset()`, sets the current position back to the start position and clears both directions.

    > **Note:** The direction buffer lets the game check that a direction is valid before the entity actually takes it.

    - `Ghost` adds three attributes: its identifier `name`, its state `frightened` and its previous cell `prev` (so a frightened ghost doesn't turn straight back). Its `reset()` calls `super().reset()` and also clears `prev` and `frightened`. `image()` returns `"frightened"` or the ghost's name.
    - `PacMan` adds a `lives` counter. `image()` returns the sprite facing his current direction (`pacman_up`, `pacman_left`, ...), or `pacman` before he starts moving.

### 1.2. Maze

`Maze` is the core class in terms of algorithms and data structures. It has four main methods and several important attributes:

**Attributes**

- `grid` stores the maze (initially defined as an array of strings) as a matrix.
- `pacman_graph` maps each traversable cell to the adjacent cells PacMan can move to.
- `ghost_graph` is the same, except that ghosts can also traverse `-`, which is why a separate graph is needed.
- `pellets` and `power_pellets` are sets with the positions of the `.` and `o` cells.

**Methods**

- **`parse()`** loops through the `MAZE` defined in constants and:
    - finds each ghost, creates a `Ghost` object with its name and position, and appends it to `ghosts`. The `G` symbol is replaced with an empty space `" "`. Names are assigned in the order the ghosts are found, taken from `GHOSTS` in **constants.py**.
    - finds PacMan, creates a `PacMan` object with its position, and replaces `P` with `" "`.
    - adds each `.` to the `pellets` set and each `o` to the `power_pellets` set, and replaces them with `" "`.

    > **Note:** Entities and pellets are replaced with whitespace because the grid should only contain the maze itself.

- **`neighbors()`** takes a position in the grid and checks which adjacent positions an entity can traverse. It is a helper for `build_graph()`.
    - Ghosts can traverse everything except `#`.
    - PacMan can traverse everything except `#` and `-`.

- **`build_graph()`** builds the adjacency map `graph` from the grid in three steps:
    1. Map each traversable cell of the `grid` to an empty list (what is traversable depends on whether the graph is for ghosts, which is passed as a boolean).
    2. For each key (a position tuple), extend its list with the key's neighbors.
    3. Return the graph.

- **`build_weighted_graph()`** builds the ghost graph again, but each connection is a `(neighbor, cost)` tuple: stepping onto a cell costs 1, or `GHOST_COST` (20, in **constants.py**) if a ghost is standing on it. It is rebuilt every time the ghosts move, because the ghosts' positions change.

### 1.3. Pathfinding

**pathfinding.py** has one data structure and two algorithms:

- `QueueLinkedList` is our queue from session 13, built on a linked list of `Node`s. `enqueue()` and `dequeue()` are both O(1).
- `bfs()` (*breadth-first search*) returns the first step an entity should take towards a target, as a position and not a direction. It uses `QueueLinkedList` and a `parent` dictionary that is also the visited set. Blinky uses it.
- `dijkstra()` is the class version: a priority queue (`heapq`) of `(distance, cell)` tuples and a `distances` dictionary. It returns the distance from the start to every cell. Pinky and Inky use it.

**Why two algorithms?** BFS is optimal when every step costs the same, which is true for Blinky. Pinky and Inky avoid the cells of the other ghosts, so their steps have different costs, and BFS would give wrong answers. Dijkstra is needed for that. Without it, all three ghosts followed the same BFS path in a line, and since ghosts can pass through each other, two BFS ghosts on the same cell would move as one from then on. We tried a cost of 5 first, but the ghosts still bunched up in the corridors, so we raised it to 20.

### 1.4. Game

The `Game` class mixes functional logic and game logic.

**Functional Logic**

- **`on_key()`** handles key presses registered by `game2dboard`. If the key is a valid direction (a key of the `DIRS` dictionary), it sets the `next_direction` of the `PacMan` object to it.
- **`tick()`** runs each time the `game2dboard` timer fires, every `TICK_MS` milliseconds (set in **constants.py**).

**Game Logic**

- **`tick()`** runs in this order:
    1. Move PacMan. If he walked into a ghost, stop here.
    2. If both pellet sets are empty, stop the timer and display `"You win! Score: X"`.
    3. Count down the power pellet with `update_frightened()`.
    4. Every second tick, move the released ghosts. The middle ghost (Blinky) sits right below the door, so he is released first (after tick 2), then Pinky (after tick 20), then Inky (after tick 40). `dijkstra()` runs once from PacMan's position and the distances are shared by Pinky and Inky. If a ghost catches PacMan, the tick stops so the other ghosts don't move off their reset positions.
- **`pacman_move()`** first checks that `next_direction` is set (which only happens once the user starts playing) and that the direction is valid. If both hold, that direction becomes the current direction; otherwise the direction is left unchanged. A second block then updates PacMan's position and the eaten pellets, renders the new positions, and checks for collisions. It returns `True` if PacMan died.
- **`ghost_move()`** moves a ghost one step:
    - Frightened ghosts take a random neighbor (`random_step()`), but not straight back to `prev` if there is another way.
    - Blinky takes the next step of the `bfs()` path towards PacMan.
    - Pinky and Inky take the neighbor with the smallest Dijkstra distance (`closest_neighbor()`).

    Ghosts can pass through each other. It calls `check_collision()` to detect a catch, and returns `True` if PacMan died.
- **`check_collision()`** checks whether a ghost and PacMan are on the same cell. A frightened ghost is eaten (200 points, back to the ghost house); otherwise it calls `lose_life()` and returns `True`.
- **`frighten()`** runs when PacMan eats a power pellet: every ghost becomes frightened for `FRIGHTENED_TICKS` (40) ticks. **`update_frightened()`** counts down and turns them back to normal.
- **`lose_life()`** subtracts 1 from the `lives` counter, clears the frightened timer and resets every entity. When PacMan runs out of lives, it stops the timer and displays `"Game Over! Score: X"`.
- **`next_pos()`** takes a position and a direction and returns the position one cell further in that direction, wrapping around at the tunnels.
- **`can_move()`** checks whether the next position in a given direction is among the traversable neighbors of PacMan's current position in `pacman_graph`.
- **`eat()`** checks whether PacMan's new position is in `pellets` or `power_pellets` (O(1) set lookups). If so, it removes it from the set and adds its points to the score (10 or 50). A power pellet also calls `frighten()`.

### 1.5. Render

`Render` is the least relevant class, as it mainly handles displaying the game, which isn't part of the grading criteria. Still, it helps to understand how it works:

- **`draw()`** calls `draw_cell()` for every cell of the grid.
- **`draw_cell()`** updates a single cell of the `Board`, which is more efficient than redrawing everything. It draws PacMan (facing his direction) or a ghost if one is there, otherwise a pellet if the position is in one of the sets, otherwise the maze tile.

Images are stored in the **img** folder next to the script you run. The dictionary `IMAGES` maps each grid symbol or entity to its image.

### 1.6. Data structures

- **2D array** (list of lists) for the maze `grid`.
- **Dictionaries** (hash tables) for the adjacency lists `pacman_graph` and `ghost_graph`, the BFS `parent` map and the Dijkstra `distances`.
- **Sets** for `pellets` and `power_pellets`: checking and removing a pellet is O(1).
- **Our own queue** (`QueueLinkedList`) for BFS.
- **Heap / priority queue** (`heapq`) for Dijkstra.

### 1.7. What we abandoned

An autoplayer. It needed a BFS for every neighbor of every cell, per ghost, every tick (about 1,242 searches per tick), and it was a random walk that couldn't win. It didn't add anything to the game, so we removed it together with `bfs_distance()`.

## 2. Imports

- **External:** `game2dboard` (version 0.8), used in **render.py** for the board and window.
- **Standard library:** `heapq` (the Dijkstra priority queue in **pathfinding.py**) and `random` (frightened ghosts in **game.py**).
- **Project files:** each file imports what it needs from the others, e.g. **game.py** imports `Maze`, `Render` and `bfs`.

## 3. Running the Code

This requires Python 3.10 or newer. With [uv](https://docs.astral.sh/uv/), from the repository root, run:

```
uv run python v2/game.py
```

Dependencies are installed automatically on the first run. Without uv, install the library and just run the file:

```
pip install game2dboard==0.8
python v2/game.py
```

Control PacMan with the arrow keys. Eat every pellet to win; a power pellet lets you eat the ghosts for a few seconds.
