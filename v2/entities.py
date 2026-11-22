class Entity(): 
    def __init__(self, pos):
        self.pos = pos
        self.start = pos
        self.direction = None
        self.next_direction = None

    def reset(self):
        self.pos = self.start 
        self.direction = None
        self.next_direction = None

class PacMan(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.lives = 3


class Ghost(Entity):
    def __init__(self, pos, name):
        super().__init__(pos)
        self.name = name 
        self.frightened = False
        self.prev = None        # previous cell, so a frightened ghost doesn't turn straight back

    def reset(self):
        super().reset()
        self.prev = None
        self.frightened = False

    @property
    def image(self):
        return "frightened" if self.frightened else self.name
    