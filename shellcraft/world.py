
class World:

    max_y = 10
    max_x = 10

    def __init__(self, stdscr):
        self.map = []
        self.stdscr = stdscr

    def generate(self):
        for j in range(World.max_y):
            tmp = []
            for i in range(World.max_x):
                tmp.append(j * 10 + i)

            self.map.append(tmp)

    # Safely draws a block at a given position
    def draw(self, y, x, block_y, block_x):
        block = self.map[block_y % World.max_y][block_x % World.max_x]
        # block.draw(y, x)
        self.stdscr.addstr(y, x, "{}".format(block))

        return 0
