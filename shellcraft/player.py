from .enums.direction import Direction
from . import blocks
from .utils.chilog import chilog

class Player:

    def __init__(self):
        self.y = 0
        self.x = 0
        self.item = "DIRT"
        self.originalBlockType = "AIR"
        self.action = "PLACE"
        self.health = 3

    def coords(self):
        return self.y, self.x

    def handle_player_move(self, c, world, stdscr):
        chilog('1')
        """
        PLAYER CONTROLS:

        W - MOVE UP
        S - MOVE DOWN
        A - MOVE LEFT
        D - MOVE RIGHT

        X - TOGGLE ACTION BREAK 
        Z - TOGGLE ACTION PLACE 

        I - PLACE/BREAK BLOCK UP
        J - PLACE/BREAK BLOCK LEFT
        K - PLACE/BREAK BLOCK DOWN
        L - PLACE/BREAK BLOCK RIGHT
        """

        # Debug
        debug = False

        if (c == ord(' ') and debug):
            chilog("Y: " + str(self.y) + " X: " + str(self.x))

        elif (c == ord('z')): #Placeing mode 
            self.action = "PLACE"
        
        elif (c == ord('x')):
            self.action = "BREAK"

        # Movement 
        elif (c == ord('d')): # Move Right
            if (self.move_legal(Direction.RIGHT, world) or debug):
                self.x += 1
        elif (c == ord('a')): # Move Left
            if (self.move_legal(Direction.LEFT, world) or debug):
                self.x -= 1
        elif (c == ord('w')): # Move Up
            if (self.move_legal(Direction.TOP, world) or debug):
                self.y -= 1
        elif (c == ord('s')): #Move Down 
            if (self.move_legal(Direction.BOTTOM, world) or debug):
                self.y += 1

        # Block action
        elif (c == ord('l')): #Place block right
            if (self.action == "PLACE"):
                if (self.place_legal(Direction.RIGHT, world)):
                    self.place_block(Direction.RIGHT, world, stdscr)
            if (self.action == "BREAK"):
                self.break_block(Direction.RIGHT, world, stdscr)

        elif (c == ord('j')): #Place block right
            if (self.action == "PLACE"):
                if (self.place_legal(Direction.LEFT, world)):
                    self.place_block(Direction.LEFT, world, stdscr)
            if (self.action == "BREAK"):
                self.break_block(Direction.LEFT, world, stdscr)

        elif (c == ord('i')): #Place block right
            if (self.action == "PLACE"):
                if (self.place_legal(Direction.TOP, world)):
                    self.place_block(Direction.TOP, world, stdscr)
            if (self.action == "BREAK"):
                self.break_block(Direction.TOP, world, stdscr)

        elif (c == ord('k')): #Place block right
            if (self.action == "PLACE"):
                if (self.place_legal(Direction.BOTTOM, world)):
                    self.place_block(Direction.BOTTOM, world, stdscr)
            if (self.action == "BREAK"):
                self.break_block(Direction.BOTTOM, world, stdscr)

        # Inventory 
        elif (c == ord('1')): # Inventory 1
            self.item = "DIRT"
        elif (c == ord('2')): # Inventory 1
            self.item = "COMP"
        elif (c == ord('3')): # Inventory 1
            self.item = "WIRE_LRTB"
        elif (c == ord('4')): # Inventory 2
            self.item = "STONE"

    

    # Movement Legality     
    def move_legal(self, dir, world):
        blocktype = ""
        if (dir == Direction.LEFT):
            blocktype = world.get_block_from_pos(self.y, self.x - 1).blocktypestr
        elif (dir == Direction.BOTTOM): 
            blocktype = world.get_block_from_pos(self.y + 1, self.x).blocktypestr
        elif (dir == Direction.RIGHT): 
            blocktype = world.get_block_from_pos(self.y, self.x + 1).blocktypestr
        elif (dir == Direction.TOP):
            blocktype = world.get_block_from_pos(self.y - 1, self.x).blocktypestr

        if (blocktype == "WATER" or blocktype == "AIR" or "WIRE" in blocktype):
            return True 
        else:
            return False 


    # Block placement legality 
    def place_legal(self, dir, world):
        blocktype = ""
        if (dir == Direction.LEFT):
            blocktype = world.get_block_from_pos(self.y, self.x - 1).blocktypestr
        elif (dir == Direction.BOTTOM): 
            blocktype = world.get_block_from_pos(self.y + 1, self.x).blocktypestr
        elif (dir == Direction.RIGHT): 
            blocktype = world.get_block_from_pos(self.y, self.x + 1).blocktypestr
        elif (dir == Direction.TOP):
            blocktype = world.get_block_from_pos(self.y - 1, self.x).blocktypestr

        if (blocktype == "WATER" or blocktype == "AIR"):
            return True 
        else:
            return False 

    def place_block(self, dir, world, stdscr):
        if (dir == Direction.LEFT):
            world.map[self.y][self.x - 1] = blocks.Block(self.item, stdscr, self.y, self.x - 1)
        elif (dir == Direction.BOTTOM): 
            world.map[self.y + 1][self.x] = blocks.Block(self.item, stdscr, self.y + 1, self.x)
        elif (dir == Direction.RIGHT): 
            world.map[self.y][self.x + 1] = blocks.Block(self.item, stdscr, self.y, self.x + 1)
        elif (dir == Direction.TOP):
            world.map[self.y - 1][self.x] = blocks.Block(self.item, stdscr, self.y - 1, self.x)

    def break_block(self, dir, world, stdscr):
        if (dir == Direction.LEFT):
            world.map[self.y][self.x - 1] = blocks.Block("AIR", stdscr, self.y, self.x - 1)
        elif (dir == Direction.BOTTOM): 
            world.map[self.y + 1][self.x] = blocks.Block("AIR", stdscr, self.y + 1, self.x)
        elif (dir == Direction.RIGHT): 
            world.map[self.y][self.x + 1] = blocks.Block("AIR", stdscr, self.y, self.x + 1)
        elif (dir == Direction.TOP):
            world.map[self.y - 1][self.x] = blocks.Block("AIR", stdscr, self.y - 1, self.x)