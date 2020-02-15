from . import blocks

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
                stone = blocks.Block("SAND", self.stdscr)
                tmp.append(stone)

            self.map.append(tmp)

    # Safely draws a block at a given position
    def draw(self, y, x, block_y, block_x):
        if 0 <= block_y and block_y < World.max_y:
            
            block = self.map[block_y][block_x % World.max_x]
            block.draw(y, x)

            return 0
        
        return -1
