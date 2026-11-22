class PacMan():
    def __init__(self, pos):
        self.pos = pos
        self.start = pos
        self.direction = None
        self.next_direction = None      # direction buffer: the last key pressed
        self.lives = 3

    def reset(self):
        self.pos = self.start
        self.direction = None
        self.next_direction = None

    def image(self):
        # face the way Pac-Man is moving (pacman_up.png, pacman_left.png, ...)
        if self.direction is None:
            return "pacman"
        else:
            return "pacman_" + self.direction.lower()


class Ghost():
    def __init__(self, pos, name):
        self.pos = pos
        self.start = pos
        self.name = name
        self.frightened = False
        self.prev = None        # previous cell, so a frightened ghost doesn't turn straight back

    def reset(self):
        self.pos = self.start
        self.prev = None
        self.frightened = False

    def image(self):
        if self.frightened:
            return "frightened"
        else:
            return self.name
