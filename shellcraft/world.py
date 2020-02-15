
class World:

    max_y = 100
    max_x = 100

    def __init__(self, stdscr):
        self.map = [[]]
        self.stdscr = stdscr

    def generate(self):
        self.map = [["."] * 100] * 100

    # Safely draws a block at a given position
    def draw(self, y, x):
        try:
            if 0 <= y and y < World.max_y:
                if 0 <= x and y < World.max_x:

                    block = self.map[y // 3][x // 3]
                    # block.draw(y, x)
                    self.stdscr.addstr(y, x, block)

                    return 0

        except IndexError:
            return -2

        return -1
