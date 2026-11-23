# Algorithms and Data Structures – Group Project: Pac-Man

## 1. Object-Oriented Structure

The program is structured in 6 classes and one function, distributed across 5 files:

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

    - `Ghost` adds three attributes: its identifier `name`, its state `frightened` and its previous cell `prev` (so a frightened ghost doesn't turn straight back). `image()` returns `"frightened"` or the ghost's name.
    - `PacMan` adds a `lives` counter. `image()` returns the sprite facing his current direction (`pacman_up`, `pacman_left`, ...), or `pacman` before he starts moving.

### 1.2. Maze

`Maze` is the core class in terms of algorithms and data structures. It has four main methods and several important attributes:

**Attributes**

- `grid` stores the maze (initially defined as an array of strings) as a matrix.
- `pacman_graph` maps each traversable cell to the adjacent cells PacMan can move to.
- `ghost_graph` is the same, except that ghosts can also traverse `-`, which is why a separate graph is needed.
- `pellets_left` counts the pellets and power pellets still in the grid.

**Methods**

- **`parse()`** loops through the `MAZE` defined in constants and:
    - finds each ghost, creates a `Ghost` object with its name and position, and appends it to `ghosts`. The `G` symbol is replaced with an empty space `" "`. Names are assigned in the order the ghosts are found, taken from `GHOSTS` in **constants.py**.
    - finds PacMan, creates a `PacMan` object with its position, and replaces `P` with `" "`.
    - counts every `.` and `o` in `pellets_left`. The pellets stay in the grid.

    > **Note:** Entities are replaced with whitespace because the grid should not contain them. Pellets stay, because they are part of the maze until PacMan eats them.

- **`neighbors()`** takes a position in the grid and checks which adjacent positions an entity can traverse. It is a helper for `build_graph()`.
    - Ghosts can traverse everything except `#`.
    - PacMan can traverse everything except `#` and `-`.

- **`build_graph()`** builds the adjacency map `graph` from the grid in three steps:
    1. Map each traversable cell of the `grid` to an empty list (what is traversable depends on whether the graph is for ghosts, which is passed as a boolean).
    2. For each key (a position tuple), extend its list with the key's neighbors.
    3. Return the graph.


### 1.3. Pathfinding

**pathfinding.py** has one function:

- `bfs()` (*breadth-first search*) returns the first step an entity should take towards a target, as a position and not a direction. It uses a `deque` as the queue and a `parent` dictionary that is also the visited set. At the end it starts at the target and keeps moving to the parent until the parent is the origin; that cell is the first step. Every ghost uses it to chase PacMan.

**Why BFS?** Every step in the maze costs the same, so BFS (which explores level by level) always finds the shortest path.

### 1.4. Game

The `Game` class mixes functional logic and game logic.

**Functional Logic**

- **`on_key()`** handles key presses registered by `game2dboard`. If the key is a valid direction (a key of the `DIRS` dictionary), it sets the `next_direction` of the `PacMan` object to it.
- **`tick()`** runs each time the `game2dboard` timer fires, every `TICK_MS` milliseconds (set in **constants.py**).

**Game Logic**

- **`tick()`** runs in this order:
    1. Move PacMan. If he walked into a ghost, stop here.
    2. If `pellets_left` is 0, stop the timer and display `"You win! Score: X"`.
    3. Count down the power pellet with `update_frightened()`.
    4. Every second tick, move the released ghosts. The middle ghost (Blinky) sits right below the door, so he is released first (after tick 2), then Pinky (after tick 20), then Inky (after tick 40). If a ghost catches PacMan, the tick stops so the other ghosts don't move off their reset positions.
- **`pacman_move()`** first checks that `next_direction` is set (which only happens once the user starts playing) and that the direction is valid. If both hold, that direction becomes the current direction; otherwise the direction is left unchanged. A second block then updates PacMan's position and the eaten pellets, renders the new positions, and checks for collisions. It returns `True` if PacMan died.
- **`ghost_move()`** moves a ghost one step:
    - Frightened ghosts take a random neighbor (`random_step()`), but not straight back to `prev` if there is another way.
    - Otherwise the ghost takes the next step of the `bfs()` path towards PacMan.

    If another ghost is on that next cell (`occupied()`), the ghost waits this tick. It calls `check_collision()` to detect a catch, and returns `True` if PacMan died.
- **`check_collision()`** checks whether a ghost and PacMan are on the same cell. A frightened ghost is eaten (200 points, back to the ghost house); otherwise it calls `lose_life()` and returns `True`.
- **`frighten()`** runs when PacMan eats a power pellet: every ghost becomes frightened for `FRIGHTENED_TICKS` (40) ticks. **`update_frightened()`** counts down and turns them back to normal.
- **`lose_life()`** subtracts 1 from the `lives` counter. If it reaches 0, it stops the timer and displays `"Game Over! Score: X"` without starting a new life. Otherwise it clears the frightened timer, resets every entity (positions, PacMan's directions, the ghosts' `frightened` and `prev`) and updates the title.
- **`update_title()`** shows the score and lives in the window title. It runs at the start, after every move and after every death, so the lives counter is always current.
- **`next_pos()`** takes a position and a direction and returns the position one cell further in that direction, wrapping around at the tunnels.
- **`can_move()`** checks whether the next position in a given direction is among the traversable neighbors of PacMan's current position in `pacman_graph`.
- **`eat()`** checks whether PacMan's new position holds a pellet (`.`) or a power pellet (`o`) in the grid. If so, it removes it from the grid, subtracts 1 from `pellets_left` and adds its points to the score (10 or 50). A power pellet also calls `frighten()`.
- **`occupied()`** returns `True` if a ghost is on the given cell, so ghosts don't overlap.

### 1.5. Render

`Render` is the least relevant class, as it mainly handles displaying the game, which isn't part of the grading criteria. Still, it helps to understand how it works:

- **`draw()`** calls `draw_cell()` for every cell of the grid.
- **`draw_cell()`** updates a single cell of the `Board`, which is more efficient than redrawing everything. It draws PacMan (facing his direction) or a ghost if one is there, otherwise the maze tile (wall, door, pellet, power pellet or empty).

Images are stored in the **img** folder next to the script you run. The dictionary `IMAGES` maps each grid symbol or entity to its image.

### 1.6. Data structures

- **2D array** (list of lists) for the maze `grid`.
- **Dictionaries** (hash tables) for the adjacency lists `pacman_graph` and `ghost_graph` and the BFS `parent` map.
- **Queue** (`deque`) for BFS: adding at the back and taking from the front are both O(1).
- **Counter** `pellets_left` for the win condition.

### 1.7. What we abandoned

An autoplayer. It needed a BFS for every neighbor of every cell, per ghost, every tick (about 1,242 searches per tick), and it was a random walk that couldn't win. It didn't add anything to the game, so we removed it together with `bfs_distance()`.

## 2. Imports

- **External:** `game2dboard` (version 0.8), used in **render.py** for the board and window.
- **Standard library:** `collections.deque` (the BFS queue in **pathfinding.py**) and `random` (frightened ghosts in **game.py**).
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
