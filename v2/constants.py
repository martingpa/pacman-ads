MAZE = [
    "###################",
    "#........#........#",
    "#o##.###.#.###.##o#",
    "#.................#",
    "#.##.#.#####.#.##.#",
    "#....#...#...#....#",
    "####.### # ###.####",
    "####.#       #.####",
    "####.# ##-## #.####",
    "    .  #GGG#  .    ",
    "####.# ##### #.####",
    "####.#       #.####",
    "####.# ##### #.####",
    "#........#........#",
    "#.##.###.#.###.##.#",
    "#o.#.....P.....#.o#",
    "##.#.#.#####.#.#.##",
    "#....#...#...#....#",
    "#.######.#.######.#",
    "#.................#",
    "###################",
]

GHOSTS = ["pinky", "blinky", "inky"]    # names in the order parse() finds the G cells, so Blinky is the middle one
DIRS = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
TICK_MS = 200
FRIGHTENED_TICKS = 40   # how long a power pellet lasts
GHOST_COST = 20     # cost of a cell with a ghost on it (a normal cell costs 1). With 5 the ghosts still queued in corridors

