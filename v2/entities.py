class Entity(): 
    def __init__(self, pos):
        self.pos = pos
        self.start = pos
        self.direction = None
        self.next_direction = None

    def reset(self):
        self.pos = self.start 

class PacMan(Entity):
    def __init__(self, pos):
        super().__init__(pos)
        self.lives = 3


class Ghost(Entity):
    def __init__(self, pos, name):
        super().__init__(pos)
        self.name = name 
        self.frightened = False


    @property
    def image(self):
        return "frightened" if self.frightened else self.name
    