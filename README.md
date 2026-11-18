# Algorithms and Data Structures - Group Project - PACMAN

## 1- Object Oriented Strucutre

The program is strucutred in 6 classes and one function, distributed in 6 files: 

- ``Entity`` within **entities.py**
    - *``PacMan``* (inherits attributes from `Entity`) within **entities.py**
    - *``Ghost``* (inherits attributes from `Entity`) within **entities.py**
- `Maze` within **maze.py**
- `Game` within **game.py**
- `Render` within **render.py**
- the *function* `bfs()` within **pathfinding.py**

An additional **constants.py** file also exists. 

### 1.1- Entities

There are two entity types within the game: 

- PacMan
- The Ghosts

Each one is represented by their corresponding classes `PacMan` and `Ghost` which inherit the attributes from the `Entity` Class. 

- ``Entity`` has two attributes: current position `pos`, and start position `start`. It has one method `reset` which sets the current position to the start position. 
    - `Ghost` inherits the attributes of ``Entity`` but has two other attributes: the identifier of the ghost `name`, and the state of the ghost `frightened`.
    - `PacMan` inherits the attributes of ``Entity`` but has three other attributes: the direction in which its moving `direction`, the direction buffer which holds the next direction `next_direction` and the number of lives remaining `lives`. The direction buffer is used to check if a direction is valid before the entity takes that direction. 

The Maze itself is also an object, instance of the `Maze` class 

### 1.2- Maze

The `Maze` class is the foundational class in terms of algorithms and data structures. It contains three main methods and several important attributes: 

**Attributes**

- `grid` this attribute stores the maze (which is initially defined as an array of strings) as a matrix. 
- `pacman_graph` is the graph which maps each traversable cell to the adjacent cells that PacMan could traverse. 
- `ghost_graph` is the same except ghosts can also traverse `-`, hence theres a different graph. 

**Methods**

- `parse()`: this method loops through the `MAZE` defined in constants and does multiple things: 
    - Identifies the position of each ghost and appends to the `ghosts` attribute each corresponding ghost object with their name and position, then it replaces the ghost symbol `G` with an empty space `" "`. The name is assigned based on which ghost is identified first. The names are defined in `GHOSTS` within **constants.py**. 
    - Identifies the position of PacMan and creates a `PacMan` object with its position. Then its symbol `P` is replaced with `" "`
        - PacMan and The Ghosts are identified and replaced with whitespace in the `grid` attribute since the grid should not contain the entities. 

- `neighbors()`: this method takes a position in the grid and checks which adjacent positions an entity could traverse. It acts as a helper for the next method `build_graph` 
    - Ghosts can traverse everything except `#`
    - PacMan can traverse everything except `#` or `-`.

- `build_graph()`: this method builds a graph out of the grid. 
    - `graph` is the adjacency map. 

    - It first maps each traversable cell of the `grid` (which varies between ghost or not ghost, which is passed as a boolean) to an empty array.
    - Then for every key in the dictionary it extends the array with all the neighbors of the key (which is a position tuple)
    - Then it returns the graph. 

### 1.3- `bfs` in **pathfinding.py**

### 1.4- Game 

The `Game` class defines a mixture of game logic and functional logic. 

**Functional Logic**

- `on_key()` defines the behaviour of the game when the module `game2dboard` registers a keystroke. In this case, it checks if the keystroke corresponds to an admitted direction (stored in the dictionary `DIRS`) and if it does, it sets the `next_direction` attribute of the `PacMan` object to it. 
- `tick()` defines what happens every time the `game2dboard` timer repeats a number of `TICKS` specified in **constants.py**. The behaviour that occurs is very important:
    - First it checks if theres a next_direction and if that next_direction is valid. If it is it makes the direction equal to the next_direction. 
    - Next, if a direction exists (that is, if in the previous conditional both conditions where ``True``) it does the following:
        - It records the old position of PacMan
        - Updates the position of PacMan according to the direction (moves one cell in the correct direction)
        - Calls the `eat()` method which cehcks if theres any prize to claim. 
        - Then it renders the maze and the entities. **\* Check **render.py** to see render logic**

**Game Logic**

- `next_pos()` takes a position and a direction as an argument and returns the updated position (one cell in the corresponding direction). It wraps the position around the tunnels. 
- `can_move()` checks if the next_position in the direction of PacMan is in the array that holds the traversable positions from the current position of PacMan. This array is mapped by `graph_pacman` from the current position.
- `eat()` checks if the current position of PacMan (after moving) corresponds with the position of some prize like a pellet. If it does it removes the prize from the grid before rendering and adds the prize to the score. 

