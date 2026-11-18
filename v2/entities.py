class Entity(): 
    def __init__(self, pos):
        self.pos = pos
        self.start = pos

    def reset(self):
        self.pos = self.start 

class PacMan(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.lives = 3
        self.direction = None
        self.next_direction = None

class Ghost(Entity):
    def __init__(self, pos, name):
        super().__init__(pos)
        self.name = name 
        self.frightened = False
        self.direction = None

    @property
    def image(self):
        return "frightened" if self.frightened else self.name
    