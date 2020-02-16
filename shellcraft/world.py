from . import blocks
import math
import random

class World:

    max_y = 30
    max_x = 300

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

         # Lake generation
       
        lake_x = set()
        checked = set()
        for num_bumps in range(max(1, (World.max_x // 20))):
            lake_x.add(random.randint(0, World.max_x-1))
       
        for x in lake_x :
            checked.add((10,x))
            prob = 0.85
            limit = 23
            self.map[7][x] = blocks.Block("WATER", self.stdscr, 7, x)
            self.convert_lake(7, x+1, prob, limit, checked)
            self.convert_lake(7, x-1, prob, limit, checked)
            self.convert_lake(8, x, prob, limit, checked)
            checked.clear()
           
        # Mountain generation
        i = 0
        viable_land = []
       
        # below loop works but make more efficient?
        while (i < World.max_x) :
            j = i
            while(i < World.max_x and self.map[7][i].blocktypestr == "DIRT"):
                i += 1
            if (j != i) :
                viable_land.append((j, i)) # i is first non-dirt block
            i += 1
       
        # Count number of hilltops per viable land
        for x in viable_land :
            len_land = x[1] - x[0]
            hilltop_bound = int(2 + ((len_land-0.1) // 10))
            hilltop_count = math.floor(random.random()**0.25 * hilltop_bound)
           
           
           
            hilltops = []
            for i in range(hilltop_count) :
                # Max height defined as 6 + log(length)
                # Use -(x-shift)^2 + 1 as distriution, where shift = -e^-(length + 1 - hilltop_count) + 1
                # As length is larger and larger, the more the distribution shifts towards max height
                max_height = math.ceil(2 + math.log(len_land))
               
                dist_shift = (-1 * 1.4**(-1 * (len_land + 1 - hilltop_count**1.5))) + 1
                height = max_height * ((-1 * ((random.random() - dist_shift) ** 2)) + 1)
                height = math.floor(height)
                hilltops.append((height, random.randint(x[0], x[1]-1)))
                hilltop_x = int(random.randrange(x[0], x[1]))
                for j in range(max(0, 9 - height), 10) :
                    self.map[j][hilltop_x] = blocks.Block("DIRT", self.stdscr, j, hilltop_x)
           
       
        # Covering with grass
       
        # Initial computer generation
       
        self.map[0][0] = blocks.Block("COMP", self.stdscr, 0, 0)
        self.map[0][0] = blocks.Block("ZEROZERO", self.stdscr, 0, 0)
        self.map[0][1] = blocks.Block("ZEROONE", self.stdscr, 0, 1)
        self.map[1][0] = blocks.Block("ONEZERO", self.stdscr, 1, 0)
   
    def convert_lake(self, y, x, prob, limit, checked) :
        x = x % World.max_x
        if (limit <= 0) :
            return
        elif ((y,x) in checked) :
            return
        elif (y < 0 or y > World.max_y) :
            return
        checked.add((y, x))
        self.map[y][x] = blocks.Block("WATER", self.stdscr, y, x)
        if (random.random() < prob) :
            dec = 0.9
            self.convert_lake(y,x-1, prob * dec, limit-1, checked)
            self.convert_lake(y, x+1, prob * dec, limit-1, checked)
            self.convert_lake(y+1, x, prob * dec, limit-1, checked)
            extra = random.random()
            if(extra < 0.3) :
                self.convert_lake(y+2, x, prob * dec, limit-1, checked)
            elif(extra < 0.55) :
                self.convert_lake(y, x-2, prob * dec, limit-1, checked)
                self.convert_lake(y, x+2, prob * dec, limit-1, checked)
        return


    def spawn(self):
        """
        Returns initial player coordinate
        """

        return 6,0



    # Safely draws a block at a given position
    def draw(self, y, x, block_y, block_x):
        if 0 <= block_y and block_y < World.max_y:
            
            block = self.map[block_y][block_x % World.max_x]
            block.draw(y, x)

            return 0
        
        return -1

    def get_block_from_pos(self, y, x): 
        """
        y, x: index of block
        """
        return self.map[y][x % World.max_x] # wraping