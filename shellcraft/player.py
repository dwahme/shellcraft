class Player:

    def __init__(self):
        self.y = 0
        self.x = 0

    def coords(self):
        return self.y, self.x

    def handleMovement(self, c):
        if (c == 'w'):
            self.x -= 1