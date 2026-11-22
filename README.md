# Algorithms and Data Structures – Group Project: Pac-Man

## 1. Object-Oriented Structure

The program is structured in 8 classes and several functions, distributed across 6 files:

- `PacMan` and `Ghost` in **entities.py**
- `Maze` in **maze.py**
- `Game` in **game.py**
- `Render` in **render.py**
- `Node` and `QueueLinkedList` (our queue from session 13) and `MinHeap` (our heap from session 20) in **pathfinding.py**
- the functions `bfs()`, `dfs()` and `dijkstra()` in **pathfinding.py**
- the functions `topk()`, `merge()`, `msort()`, `bsearch()` and `save_score()` in **scores.py**

An additional **constants.py** file also exists.

### 1.1. Entities

There are two entity types within the game:

- PacMan
- The Ghosts

Each is represented by its own plain class, `PacMan` and `Ghost`, written the same way as the classes from our notebooks (like `Node` and `QueueLinkedList`).

- `PacMan` has the current position `pos`, the start position `start`, the current direction `direction`, the direction buffer `next_direction` and a `lives` counter. `reset()` sets the position back to the start and clears both directions. `image()` returns the sprite facing his current direction (`pacman_up`, `pacman_left`, ...), or `pacman` before he starts moving.

    > **Note:** The direction buffer lets the game check that a direction is valid before PacMan actually takes it.

- `Ghost` has `pos`, `start`, its identifier `name`, its state `frightened` and its previous cell `prev` (so a frightened ghost doesn't turn straight back). `reset()` sets the position back to the start and clears `prev` and `frightened`. `image()` returns `"frightened"` or the ghost's name.

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

- **Maze check:** at the end of `__init__`, the class `dfs()` runs once from PacMan's start with no target, so it visits every cell PacMan can reach. If a pellet or power pellet was not visited, it raises an error. This guarantees the game can be won, even if someone edits `MAZE`. We use DFS because we only need to know *whether* a cell is reachable, not the shortest way there.

- **`build_weighted_graph()`** builds the ghost graph again, but each connection is a `(neighbor, cost)` tuple: stepping onto a cell costs 1, or `GHOST_COST` (20, in **constants.py**) if a ghost is standing on it. It is rebuilt every time the ghosts move, because the ghosts' positions change.

### 1.3. Pathfinding

**pathfinding.py** has two data structures and three algorithms, all from class:

- `QueueLinkedList` is our queue from session 13, built on a linked list of `Node`s. `enqueue()` and `dequeue()` are both O(1).
- `MinHeap` is our heap from session 20. `push()` and `pop()` are O(log n).
- `bfs(graph, origin, target)` (*breadth-first search*) explores the graph level by level with `QueueLinkedList`. Its `parent` dictionary is also the visited set. Blinky uses it.
- `dijkstra(graph, start, target)` is the class version on our `MinHeap` of `(distance, cell)` tuples, with a `distances` dictionary. Pinky and Inky use it.
- `dfs(graph, start, target, visited)` is the recursive depth-first search from class, used for the maze check.

`bfs()` and `dijkstra()` both return the **first step** of the path from the ghost to PacMan, as a position. Both remember each cell's `parent` (the cell they reached it from). At the end they start at the target and keep moving to the parent until the parent is the start. That cell is the first step.

**Why two algorithms?** BFS is optimal when every step costs the same, which is true for Blinky. Pinky and Inky avoid the cells of the other ghosts, so their steps have different costs, and BFS would give wrong answers. Dijkstra is needed for that. Without it, all three ghosts followed the same BFS path in a line, and since ghosts can pass through each other, two BFS ghosts on the same cell would move as one from then on. We tried a cost of 5 first, but the ghosts still bunched up in the corridors, so we raised it to 20.

### 1.4. Game

The `Game` class mixes functional logic and game logic.

**Functional Logic**

- **`on_key()`** handles key presses registered by `game2dboard`. If the key is a valid direction (a key of the `DIRS` dictionary), it sets the `next_direction` of the `PacMan` object to it.
- **`tick()`** runs each time the `game2dboard` timer fires, every `TICK_MS` milliseconds (set in **constants.py**).

**Game Logic**

- **`tick()`** runs in this order:
    1. Move PacMan. If he walked into a ghost, stop here.
    2. If both pellet sets are empty, the game ends with `end("You win!")`.
    3. Count down the power pellet with `update_frightened()`.
    4. Every second tick, move the released ghosts. The middle ghost (Blinky) sits right below the door, so he is released first (after tick 2), then Pinky (after tick 20), then Inky (after tick 40). If a ghost catches PacMan, the tick stops so the other ghosts don't move off their reset positions.
- **`pacman_move()`** first checks that `next_direction` is set (which only happens once the user starts playing) and that the direction is valid. If both hold, that direction becomes the current direction; otherwise the direction is left unchanged. A second block then updates PacMan's position and the eaten pellets, renders the new positions, and checks for collisions. It returns `True` if PacMan died.
- **`ghost_move()`** moves a ghost one step:
    - Frightened ghosts take a random neighbor (`random_step()`), but not straight back to `prev` if there is another way.
    - Blinky takes the next step of the `bfs()` path towards PacMan.
    - Pinky and Inky take the next step of the `dijkstra()` path towards PacMan. The weighted graph is built right before their own step, so it uses where the other ghosts are now (Blinky has already moved this tick). That's at most 2 Dijkstra runs per tick, each well under a millisecond.

    Ghosts can pass through each other. It calls `check_collision()` to detect a catch, and returns `True` if PacMan died.
- **`check_collision()`** checks whether a ghost and PacMan are on the same cell. A frightened ghost is eaten (200 points, back to the ghost house); otherwise it calls `lose_life()` and returns `True`.
- **`frighten()`** runs when PacMan eats a power pellet: every ghost becomes frightened for `FRIGHTENED_TICKS` (40) ticks. **`update_frightened()`** counts down and turns them back to normal.
- **`lose_life()`** subtracts 1 from the `lives` counter. If it reaches 0, the game ends with `end("Game Over!")` without starting a new life. Otherwise it clears the frightened timer, resets every entity and updates the title.
- **`end()`** stops the timer, saves the score with `save_score()` and shows the result in the title: `"Game Over! Score: X | #2 on the leaderboard"`, or `"... | Best: Y"` if the score didn't make the top 5.
- **`update_title()`** shows the score and lives in the window title. It runs at the start, after every move and after every death, so the lives counter is always current.
- **`next_pos()`** takes a position and a direction and returns the position one cell further in that direction, wrapping around at the tunnels.
- **`can_move()`** checks whether the next position in a given direction is among the traversable neighbors of PacMan's current position in `pacman_graph`.
- **`eat()`** checks whether PacMan's new position is in `pellets` or `power_pellets` (O(1) set lookups). If so, it removes it from the set and adds its points to the score (10 or 50). A power pellet also calls `frighten()`.

### 1.5. Render

`Render` is the least relevant class, as it mainly handles displaying the game, which isn't part of the grading criteria. Still, it helps to understand how it works:

- **`draw()`** calls `draw_cell()` for every cell of the grid.
- **`draw_cell()`** updates a single cell of the `Board`, which is more efficient than redrawing everything. It draws PacMan (facing his direction) or a ghost if one is there, otherwise a pellet if the position is in one of the sets, otherwise the maze tile.

Images are stored in the **img** folder next to the script you run. The dictionary `IMAGES` maps each grid symbol or entity to its image.

### 1.6. Scores

**scores.py** keeps a high-score table in `scores.txt` (next to the game, one score per line). When the game ends, `save_score()`:

1. reads the old scores and adds the new one,
2. keeps only the best 5 with `topk()` (a heap, session 20),
3. puts them in order with `msort()` (mergesort, session 11) and writes them back,
4. finds where the new score landed with `bsearch()` (binary search, session 8). This works because the list is sorted.

### 1.7. Course material used

| Course topic | Where we use it |
|---|---|
| Multidimensional arrays (S14) | the maze `grid` (list of lists) |
| Hash tables and sets (S15) | dictionaries for the graphs, `parent` and `distances`; sets for the pellets and the DFS `visited` cells |
| Linked lists (S5) and queues (S13) | `QueueLinkedList` in `bfs()` |
| Heaps and priority queues (S20) | our `MinHeap` in `dijkstra()`, `topk()` for the high scores |
| Graph search: BFS, DFS, Dijkstra | Blinky (`bfs()`), the maze check (`dfs()`), Pinky and Inky (`dijkstra()`) |
| Recursion (S7) | `dfs()` and `msort()` |
| Mergesort (S11) | ordering the high scores |
| Binary search (S8) | finding the new score's place |

### 1.8. What we abandoned

An autoplayer. It needed a BFS for every neighbor of every cell, per ghost, every tick (about 1,242 searches per tick), and it was a random walk that couldn't win. It didn't add anything to the game, so we removed it together with `bfs_distance()`.

## 2. Imports

- **External:** `game2dboard` (version 0.8), used in **render.py** for the board and window.
- **Standard library:** `random` (frightened ghosts in **game.py**), `heapq` (inside the class `topk()` in **scores.py**) and `os` (the path of `scores.txt` in **scores.py**).
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
