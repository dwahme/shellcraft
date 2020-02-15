
class World:

    max_y = 100
    max_x = 100

    def __init__(self):
        self.map = [[]]

    # Safely draws a block at a given position
    def draw(self, y, x):
        try:
            if 0 <= y and y < World.max_y:
                if 0 <= x and y < World.max_x:

                    block = self.map[y][x]
                    block.draw(y, x)

                    return 0

        except IndexError:
            return -2

        return -1
