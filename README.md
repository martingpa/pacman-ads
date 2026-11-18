# Algorithms and Data Structures – Group Project: Pac-Man

## 1. Object-Oriented Structure

The program is structured in 6 classes and two functions, distributed across 5 files:

- `Entity` in **entities.py**
    - `PacMan` (inherits from `Entity`) in **entities.py**
    - `Ghost` (inherits from `Entity`) in **entities.py**
- `Maze` in **maze.py**
- `Game` in **game.py**
- `Render` in **render.py**
- the functions `bfs()` and `bfs_distance()` in **pathfinding.py**

An additional **constants.py** file also exists.

### 1.1. Entities

There are two entity types within the game:

- PacMan
- The Ghosts

Each is represented by its own class, `PacMan` and `Ghost`, and both inherit from the `Entity` class.

- `Entity` has four attributes: the current position `pos`, the start position `start`, the current direction `direction` and the direction buffer `next_direction`. Its one method, `reset()`, sets the current position back to the start position.

    > **Note:** The direction buffer lets the game check that a direction is valid before the entity actually takes it.

    - `Ghost` adds two attributes: its identifier `name` and its state `frightened`.
    - `PacMan` adds a `lives` counter.

### 1.2. Maze

`Maze` is the core class in terms of algorithms and data structures. It has four main methods and several important attributes:

**Attributes**

- `grid` stores the maze (initially defined as an array of strings) as a matrix.
- `pacman_graph` maps each traversable cell to the adjacent cells PacMan can move to.
- `ghost_graph` is the same, except that ghosts can also traverse `-`, which is why a separate graph is needed.

**Methods**

- **`parse()`** loops through the `MAZE` defined in constants and:
    - finds each ghost, creates a `Ghost` object with its name and position, and appends it to `ghosts`. The `G` symbol is replaced with an empty space `" "`. Names are assigned in the order the ghosts are found, taken from `GHOSTS` in **constants.py**.
    - finds PacMan, creates a `PacMan` object with its position, and replaces `P` with `" "`.

    > **Note:** Entities are replaced with whitespace because the grid should not contain them.

- **`neighbors()`** takes a position in the grid and checks which adjacent positions an entity can traverse. It is a helper for `build_graph()`.
    - Ghosts can traverse everything except `#`.
    - PacMan can traverse everything except `#` and `-`.

- **`build_graph()`** builds the adjacency map `graph` from the grid in three steps:
    1. Map each traversable cell of the `grid` to an empty list (what is traversable depends on whether the graph is for ghosts, which is passed as a boolean).
    2. For each key (a position tuple), extend its list with the key's neighbors.
    3. Return the graph.

- **`build_weighted_graph()`** builds a graph of the cells PacMan can traverse in which each connection carries a weight: the distance from the neighboring cell to the nearest ghost, computed with `bfs_distance()`. It is part of the autoplayer algorithm.

### 1.3. Pathfinding

Both functions in **pathfinding.py** use *breadth-first search*:

- `bfs()` returns the first step an entity should take towards a target, as a position and not a direction. It drives how the ghosts follow PacMan.
- `bfs_distance()` returns the number of steps on the shortest path to a target. It is used to build the weighted graph (part of the autoplayer algorithm).

### 1.4. Game

The `Game` class mixes functional logic and game logic.

**Functional Logic**

- **`on_key()`** handles key presses registered by `game2dboard`. If the key is a valid direction (a key of the `DIRS` dictionary), it sets the `next_direction` of the `PacMan` object to it.
- **`tick()`** runs each time the `game2dboard` timer fires, every `TICK_MS` milliseconds (set in **constants.py**).

**Game Logic**

- **`pacman_move()`** works in two modes:
    - When `auto == False`, it first checks that `next_direction` is set (which only happens once the user starts playing) and that the direction is valid. If both hold, that direction becomes the current direction; otherwise the direction is left unchanged. A second block then updates PacMan's position and the eaten pellets, checks for collisions, and renders the new positions.
    - When `auto == True`, it builds the weighted graph and moves PacMan to a random neighbor that is at least 3 cells away from every ghost. If no neighbor qualifies, it moves to the neighbor furthest from the nearest ghost. Eating, collisions and rendering work as above.
- **`ghost_move()`** uses `bfs()` to move a ghost one step towards PacMan's position. It calls `occupied()` to avoid overlapping with other ghosts and `check_collision()` to detect a catch.
- **`check_collision()`** checks whether a ghost and PacMan have collided, in which case it calls `lose_life()`.
- **`lose_life()`** subtracts 1 from the `lives` counter and resets the positions of the entities. When PacMan runs out of lives, it stops the timer and displays `"Game Over!"`.
- **`next_pos()`** takes a position and a direction and returns the position one cell further in that direction, wrapping around at the tunnels.
- **`can_move()`** checks whether the next position in a given direction is among the traversable neighbors of PacMan's current position in `pacman_graph`.
- **`eat()`** checks whether PacMan's new position holds a prize such as a pellet. If so, it removes the prize from the grid before rendering and adds its points to the score.

### 1.5. Render

`Render` is the least relevant class, as it mainly handles displaying the game, which isn't part of the grading criteria. Still, it helps to understand how it works:

- **`draw()`** loops through every element of the grid and shows the matching image in the corresponding cell of the `Board`. It then places the images of the ghosts and PacMan (which were removed from the grid during parsing) in their cells.
- **`draw_cell()`** updates a single cell of the `Board`, which is more efficient than redrawing everything.

Images are stored in the **img** folder next to the script you run. The dictionary `IMAGES` maps each grid symbol or entity to its image.

## 2. Imports

- **External:** `game2dboard` (version 0.8), used in **render.py** for the board and window.
- **Standard library:** `collections.deque` (the BFS queue in **pathfinding.py**) and `random` (the autoplayer in **game.py**).
- **Project files:** each file imports what it needs from the others, e.g. **game.py** imports `Maze`, `Render` and `bfs`.

## 3. Running the Code

This requires Python 3.14 and [uv](https://docs.astral.sh/uv/). From the repository root, run:

```
uv run python v2/game.py
```

Dependencies are installed automatically on the first run. By default the game is manual: control PacMan with the arrow keys.

**Switching from manual to auto:** at the bottom of **v2/game.py**, in the `if __name__ == "__main__":` block, change `auto = False` to `auto = True`:

```python
Game(maze, Render(maze), auto = True).run()
```
