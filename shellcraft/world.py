from . import blocks
import math
import random
import time
from .utils.chilog import chilog

class World:

    max_y = 30
    max_x = 300
    ground = 14
    dirt_depth = 3
    cave_depth = 7

    def __init__(self, stdscr, seed = None):
        self.map = []
        self.stdscr = stdscr
        self.seed = seed
        random.seed(seed)

    def generate(self):
        
        # Initial superflat world generation
        tmp = []
        for i in range(World.max_x):
            blk = blocks.Block("CLOUD", self.stdscr, 0, i)
            tmp.append(blk)
        self.map.append(tmp)
        for j in range(1, World.ground):
            tmp = []
            for i in range(World.max_x):
                blk = blocks.Block("AIR", self.stdscr, j, i)
                tmp.append(blk)
            self.map.append(tmp)
        for j in range(World.ground, World.ground+World.dirt_depth):
            tmp = []
            for i in range (World.max_x):
                b = blocks.Block("DIRT", self.stdscr, j, i)
                tmp.append(b)
            self.map.append(tmp)
        for j in range(World.ground+World.dirt_depth, World.max_y - 2):
            tmp = []
            for i in range (World.max_x):
                # If j is large, slightly increase threshold
                threshold = 0.001
                threshold += (j / World.max_y) * 0.001
                rand = random.random()

                b = blocks.Block("STONE", self.stdscr, j, i)
                if (rand < threshold): 
                    chilog("Diamond: " + str(threshold) + " > " + str(rand) + "\n")
                    b = blocks.Block("DIAMOND", self.stdscr, j, i)

                tmp.append(b)
            self.map.append(tmp)
        for j in range(World.max_y - 2, World.max_y):
            tmp = []
            for i in range (World.max_x):
                b = blocks.Block("LAVA", self.stdscr, j, i)
                tmp.append(b)
            self.map.append(tmp)


        # Lake generation
        lake_x = set()
        checked = set()
        for num_bumps in range(max(1, (World.max_x // 20))):
            lake_x.add(random.randint(0, World.max_x-1))
       
        for x in lake_x :
            checked.add((World.ground,x))
            prob = 0.85
            limit = 23
            self.map[World.ground][x] = blocks.Block("WATER", self.stdscr, World.ground, x)
            self.convert_lake(World.ground, x+1, prob, limit, checked)
            self.convert_lake(World.ground, x-1, prob, limit, checked)
            self.convert_lake(World.ground+1, x, prob, limit, checked)
            checked.clear()
           
        # Mountain generation
        i = 0
        viable_land = []
        # TODO change so that flatland at x = 0 is well detected
        while (i < World.max_x) :
            j = i
            while(i < World.max_x and self.map[World.ground][i].blocktypestr != "WATER"):
                i += 1
            if (j != i) :
                viable_land.append((j, i)) # i is first non-dirt block
            i += 1
       
        # Grabbing viable land for mountain generation
        bottom = min(World.max_y, World.ground+World.dirt_depth+3)
        checked.clear()
        for coords in viable_land :
            len_land = coords[1] - coords[0]
            hilltop_bound = int(2 + ((len_land-0.1) // 8))
            hilltop_count = math.floor(random.random()**1.5 * hilltop_bound)
           
           
            hilltops = []
            max_height = math.ceil(0.5+round(math.log(len_land,3)))
            max_height = round(max_height * (World.ground - 1) / 6)
            
            # Per hilltop in each viable land
            for i in range(hilltop_count) :
                # Max height defined as 6 + log(length)
                # Use -(x-shift)^2 + 1 as distriution, where shift = -e^-(length + 1 - hilltop_count) + 1
                # As length is larger and larger, the more the distribution shifts towards max height
               
                # TODO current height generation is botched... please give me ideas :(
                dist_shift = (-1 * 1.4**(-1 * (len_land + 1 - hilltop_count**1.5))) + 1
                height = max_height * ((-1 * ((random.random() - dist_shift) ** 2)) + 1)
                height = math.floor(height)
                
                hilltop_x = int(random.randrange(coords[0], coords[1]))
                self.make_hill(height, hilltop_x, coords[0], coords[1], World.ground - 1, max_height)
            # Dirt extension
            for i in range(math.ceil(len_land/4)) :
                dx = random.randrange(coords[0], coords[1])
                dy = random.randrange(World.ground+World.dirt_depth, bottom)
                self.convert_dirt(dy, dx, 0.9, 25, checked)
                checked.clear()
            
        # Covering exposed dirt blocks grass
        for i in range(World.max_x) :
            for j in range(World.max_y) :
                if self.map[j][i].blocktypestr == "AIR" :
                    continue
                elif self.map[j][i].blocktypestr == "WATER" :
                    break
                elif self.map[j][i].blocktypestr == "DIRT" :
                    self.map[j][i] = blocks.Block("DIRTGRASS", self.stdscr, j, i)
                    if (random.random() < 0.6):
                        self.map[j-1][i] = blocks.Block("WEEDS", self.stdscr, j-1, i)
                    break
        
        # Sand generation
        ground = World.ground
        for coord in viable_land :
            prob = 0.6
            left_ground = coord[0]
            for i in range(3) :
                left_water = (left_ground - 1) % World.max_x
                if self.map[ground][left_water].blocktypestr == "WATER" and random.random() < prob :
                    self.map[ground][left_ground] = blocks.Block("SAND", self.stdscr, ground, left_ground)
                else :
                    break
                left_ground = left_water
                prob = prob * prob
            prob = 0.6
            right_ground = coord[1] - 1
            for i in range(3) :
                right_water = (right_ground + 1) % World.max_x
                if self.map[ground][right_water].blocktypestr == "WATER" and random.random() < prob :
                    self.map[ground][right_ground] = blocks.Block("SAND", self.stdscr, ground, right_ground)
                else :
                    break
                right_ground = right_water
                prob = prob * prob
        
        # Cave generation
        self.cave_gen()
        
        # Add bedrock
        for i in range (World.max_x):
            self.map[World.max_y-1][i] = blocks.Block("BEDROCK", self.stdscr, World.max_y-1, i)
    
    
    
    ## Helper Functions
    
    '''
    Recursively creates lake given y and x position
    Input : y, x    coordinates to make lake
            prob    probability of lake extending
            limit   maximum recusion depth
            checked set of coordinates to skip
    '''
    def convert_lake(self, y, x, prob, limit, checked) :
        x = x % World.max_x
        if (limit <= 0) :
            return
        elif ((y,x) in checked) :
            return
        elif (y < 0 or y >= World.max_y) :
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
            elif(extra < 0.58 and y > World.ground) :
                self.convert_lake(y-1, x, prob * dec, limit-1, checked)
        return
    
    '''
    Recursively creates hill given y and x position of hilltop
    Input : target_y, target_x          coordinates of hilltop
            left_limit, right_limit     x coordinates of limit of the base of the hill
            current_y                   the current y coordiate to create hill, stops when current_y == target_y
            max_height                  maximum height defined by the size of base land, determines slope
    '''
    def make_hill(self, target_y, target_x, left_limit, right_limit, current_y, max_height) :
        step = current_y - target_y
        if (step <= 0) :
            return      
        total_left_step = 0
        total_right_step = 0
        for i in range(step) :
            total_left_step += math.ceil(random.random()**3 * max_height)
            total_right_step += math.ceil(random.random()**3 * max_height)
        
        # A bodge of cliff prevention
        left = max(left_limit, target_x - total_left_step)
        if left == left_limit :
            if random.random() < 0.6 and left < right_limit:
                left += 1
        right = min(right_limit-1, target_x + total_right_step)
        if right == right_limit :
            if random.random() < 0.6 and right > left_limit:
                right -= 1
        for i in range(left, right + 1) :
            self.map[current_y][i] = blocks.Block("DIRT", self.stdscr, current_y, i)
        self.make_hill(target_y, target_x, left, right, current_y-1, max_height)
    
    '''
    Recursively creates deviations in dirt-stone boundary given y and x position
    Input : y, x    coordinates to make dirt patches
            prob    probability of dirt patch extending
            limit   maximum recusion depth
            checked set of coordinates to skip
    '''
    def convert_dirt(self, y, x, prob, limit, checked) :
        x = x % World.max_x
        if (limit <= 0) :
            return
        elif ((y,x) in checked) :
            return
        elif (y < 0 or y > World.max_y) :
            return
        checked.add((y, x))
        if (self.map[y][x].blocktypestr == "WATER" or self.map[y][x].blocktypestr == "AIR") :
            return
        self.map[y][x] = blocks.Block("DIRT", self.stdscr, y, x)
        if (random.random() < prob) :
            dec = 0.8
            self.convert_dirt(y,x-1, prob * dec, limit-1, checked)
            self.convert_dirt(y, x+1, prob * dec, limit-1, checked)
            self.convert_dirt(y+1, x, prob * dec, limit-1, checked)
            self.convert_dirt(y-1, x, prob * dec, limit-1, checked)
        return
        
        
    '''
    Recursively creates caves
    '''
    def cave_gen(self) :
        cave_num = World.max_x // 30
        cave_num = random.randint(round(cave_num * 0.6), round(cave_num * 1.4))
        checked = set()
        prob = 0.9
        limit = 50
        for i in range(cave_num) :
            x = random.randrange(0, World.max_x)
            y = random.randrange(World.max_y - World.cave_depth, World.max_y-2)
            self.cave_dig(y, x, prob, limit, checked)
            checked.clear()
    
    '''
    Recursively creates a single cave system
    Input : y, x    coordinates to dig caves
            prob    probability of cave extending
            limit   maximum recusion depth
            checked set of coordinates to skip
    '''
    def cave_dig(self, y, x, prob, limit, checked) :
        x = x % World.max_x
        if (limit <= 0) :
            return
        elif ((y,x) in checked) :
            return
        elif (y < 0 or y >= World.max_y) :
            return
        checked.add((y, x))
        if self.map[y][x].blocktypestr == "WATER" :
            self.coalesce_water(y, x)
            return
        self.map[y][x] = blocks.Block("AIR", self.stdscr, y, x)
        self.map[y][(x-1) % World.max_x] = blocks.Block("AIR", self.stdscr, y, (x-1) % World.max_x)
        self.map[y][(x+1) % World.max_x] = blocks.Block("AIR", self.stdscr, y, (x+1) % World.max_x)
        if (random.random() < prob) :
            dec = 0.9
            self.cave_dig(y, x-2, prob * dec, limit-1, checked)
            self.cave_dig(y, x+2, prob * dec, limit-1, checked)
            extra = random.uniform(0.5, 1)
            extra2 = random.uniform(0.5, 1)
            determinant = random.random()
            determinant2 = random.random()
            if(determinant < 0.7) :
                if (determinant2 < 0.5) :
                    self.cave_dig(y+1, x+2, prob * dec * extra, limit-1, checked)
                    self.cave_dig(y-1, x-2, prob * dec * extra2, limit-1, checked)
                else :
                    self.cave_dig(y+1, x-2, prob * dec * extra2, limit-1, checked)
                    self.cave_dig(y-1, x+2, prob * dec * extra, limit-1, checked)
            if (determinant < 0.2) :
                if (determinant2 < 0.5) :
                    self.cave_dig(y+2, x+2, prob * dec * extra, limit-1, checked)
                    self.cave_dig(y-2, x-2, prob * dec * extra2, limit-1, checked)
                else :
                    self.cave_dig(y+2, x-2, prob * dec * extra2, limit-1, checked)
                    self.cave_dig(y-2, x+2, prob * dec * extra, limit-1, checked)
        return


        

    def spawn(self):
        """
        Returns initial player coordinate
        """

        return World.ground-1,0



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
        if (y < 0 or y >= World.max_y) :
            return None
        return self.map[y][x % World.max_x] # wraping

    def coalesce_water(self, y, x):
        """
        y and x denotes the map position of the broken block
        
        will need to check for the blocks around it (TOP, LEFT, RIGHT), and see if 
        they're a water block. If so, this block becomes water too

        Then, if the LEFT, RIGHT, BOTTOM blocks are air, call coalesce on them too
        """
        if (y < 0 or y + 1 >= World.max_y) :
            return
        block_top_type = self.get_block_from_pos(y - 1, x).blocktypestr
        block_left_type = self.get_block_from_pos(y, x - 1).blocktypestr
        block_right_type = self.get_block_from_pos(y, x + 1).blocktypestr
        
        if (block_top_type == "WATER" or block_left_type == "WATER" or block_right_type == "WATER"):
            self.map[y][x % World.max_x] = blocks.Block("WATER", self.stdscr, y, x % World.max_x)
            next_block_left_type = self.get_block_from_pos(y, x - 1).blocktypestr
            next_block_right_type = self.get_block_from_pos(y, x + 1).blocktypestr
            next_block_bottom_type = self.get_block_from_pos(y + 1, x).blocktypestr

            if (next_block_bottom_type == "LAVA"):
                self.map[y][x % World.max_x] = blocks.Block("OBSIDIAN", self.stdscr, y, x % World.max_x)
            if (next_block_right_type == "LAVA"):
                self.map[y][x % World.max_x] = blocks.Block("OBSIDIAN", self.stdscr, y, x % World.max_x)
            if (next_block_left_type == "LAVA"):
                self.map[y][x % World.max_x] = blocks.Block("OBSIDIAN", self.stdscr, y, x % World.max_x)
                

            if (next_block_left_type == "AIR"):
                self.coalesce_water(y, (x - 1) % World.max_x)
            if (next_block_right_type == "AIR"):
                self.coalesce_water(y, (x + 1) % World.max_x)
            if (next_block_bottom_type == "AIR"):
                self.coalesce_water(y + 1, x % World.max_x)

            
                
