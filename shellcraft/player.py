

class Player:

    def __init__(self):
        self.y = 0
        self.x = 0
        self.item = "DIRT"
        self.originalBlockType = "AIR"

    def coords(self):
        return self.y, self.x

    