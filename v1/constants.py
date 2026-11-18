"""Game constants: maze layout, image names, directions and tuning values."""

# PARAMETERS

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

IMAGES = {"#": "wall", ".": "pellet", "o": "power", "-": "door"}
GHOSTS = ["blinky", "pinky", "inky"]
DIRS = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
TICK_MS = 200  # ms per step
GHOST_EVERY = 2  # Ghosts move once every N ticks (slower than Pac-Man)
LIVES = 3

# Points
PELLET_POINTS = 10
POWER_POINTS = 50
GHOST_POINTS = 200

FRIGHTENED_TICKS = 40  # 5 ticks = 1 s at 200 ms
