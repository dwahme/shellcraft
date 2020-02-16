from .enums.direction import Direction
from . import blocks, computer
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

    def handle_player_move(self, c, world, stdscr, game):
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
        ret = 0

        # Debug
        debug = False


        # Data 
        dir = {
            #'z': (direction, dx, dy)
            'd': (Direction.RIGHT, 1, 0),
            'a': (Direction.LEFT, -1, 0),
            'w': (Direction.TOP, 0, -1),
            's': (Direction.BOTTOM, 0, 1),
            'l': (Direction.RIGHT, 1, 0),
            'j': (Direction.LEFT, -1, 0),
            'i': (Direction.TOP, 0, -1),
            'k': (Direction.BOTTOM, 0, 1),
        }

        items = {
            '1': "DIRT",
            '2': "COMP",
            '3': "WIRE_LRTB",
            '4': "STONE",
        }

        if (c == ord(' ') and debug):
            chilog("Y: " + str(self.y) + " X: " + str(self.x))

        elif (c == ord('z')): #Placeing mode 
            self.action = "PLACE"
        
        elif (c == ord('x')):
            self.action = "BREAK"

        # Movement 
        elif (c == ord('d') or c == ord('a') or c == ord('w') or c == ord('s')):
            dir_tuple = dir[chr(c)]
            if (self.move_legal(dir_tuple, world) or debug):
                self.x += dir_tuple[1]
                self.y += dir_tuple[2]
            
        # Block action
        elif (c == ord('i') or c == ord('j') or c == ord('k') or c == ord('l')):
            dir_tuple = dir[chr(c)]
            if (self.action == "PLACE"):
                if (self.place_legal(dir_tuple, world)):
                    ret = self.place_block(dir_tuple, world, stdscr)
            if (self.action == "BREAK"):
                self.break_block(dir_tuple, world, stdscr)

        # Inventory 
        elif (c == ord('1') or c == ord('2') or c == ord('3') or c == ord('4')):
            self.item = items[chr(c)]

        return ret
        

    # Movement Legality     
    def move_legal(self, dir_tuple, world):
        blocktype = world.get_block_from_pos(self.y + dir_tuple[2], self.x + dir_tuple[1]).blocktypestr

        if (blocktype == "WATER" or blocktype == "AIR" or "WIRE" in blocktype):
            return True 
        else:
            return False 


    # Block placement legality 
    def place_legal(self, dir_tuple, world):
        blocktype = world.get_block_from_pos(self.y + dir_tuple[2], self.x + dir_tuple[1]).blocktypestr

        if (blocktype == "WATER" or blocktype == "AIR"):
            return True 
        else:
            return False 

    def place_block(self, dir_tuple, world, stdscr):
        b = blocks.Block(self.item, stdscr, self.y + dir_tuple[2], self.x + dir_tuple[1])
        world.map[self.y + dir_tuple[2]][self.x + dir_tuple[1]] = b

        if b.blocktypestr == "COMP":
            c = computer.Computer(str(len(game.computers)), b)
            game.computers.append(c)
            # c.editor(game.stdscr)

            return 1

        elif "WIRE" in b.blocktypestr:
            return 1

        return 0

    def break_block(self, dir_tuple, world, stdscr):
        world.map[self.y + dir_tuple[2]][self.x + dir_tuple[1]] = blocks.Block("AIR", stdscr, self.y + dir_tuple[2], self.x + dir_tuple[1])
        world.coalesce_water(self.y + dir_tuple[2], self.x + dir_tuple[1])
