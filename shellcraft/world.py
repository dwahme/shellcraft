from . import blocks

class World:

    max_y = 30
    max_x = 500

    def __init__(self, stdscr):
        self.map = []
        self.stdscr = stdscr

    def generate(self):
        # GENERATE CLOUDS 

        tmp = []
        for i in range(World.max_x):
            blk = blocks.Block("CLOUD", self.stdscr, 0, i)
            tmp.append(blk)

        self.map.append(tmp)

        for j in range(1, 7):
            tmp = []
            for i in range(World.max_x):
                blk = blocks.Block("AIR", self.stdscr, j, i)
                tmp.append(blk)
            self.map.append(tmp)

        for j in range(7, 8):
            tmp = []
            for i in range (World.max_x):
                b = blocks.Block("DIRTGRASS", self.stdscr, j, i)
                tmp.append(b)
            self.map.append(tmp)

        for j in range(8, 10):
            tmp = []
            for i in range (World.max_x):
                b = blocks.Block("DIRT", self.stdscr, j, i)
                tmp.append(b)
            self.map.append(tmp)

        for j in range(10, World.max_y):
            tmp = []
            for i in range (World.max_x):
                b = blocks.Block("STONE", self.stdscr, j, i)
                tmp.append(b)
            self.map.append(tmp)

        self.map[0][0] = blocks.Block("ZEROZERO", self.stdscr, 0, 0)
        self.map[0][1] = blocks.Block("ZEROONE", self.stdscr, 0, 1)
        self.map[1][0] = blocks.Block("ONEZERO", self.stdscr, 1, 0)


    def spawn(self):
        """
        Returns initial player coordinate
        """

        return 0,0
        # for y in range(World.max_y):
        #     if self.map[y][World.max_x//2].type() == "DIRTGRASS":
        #         return y-1, World.max_x//2
            
        # return 0, 0


    # Safely draws a block at a given position
    def draw(self, y, x, block_y, block_x):
        if 0 <= block_y and block_y < World.max_y:
            
            block = self.map[block_y][block_x % World.max_x]
            block.draw(y, x)

            return 0
        
        return -1
