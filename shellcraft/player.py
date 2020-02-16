from .enums.direction import Direction
from . import blocks, computer  
from .utils.chilog import chilog

class Player:

    def __init__(self):
        self.y = 0
        self.x = 0
        self.item = "DIRT"
        self.originalBlockType = "AIR"
        self.action = "NORMAL"
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
        C - TOGGLE ACTION INTERACT

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
            '5': "SAND", 
            '6': "MONITORBASIC",
            '7': "TNT"
        }

        if (c == ord(' ') and debug):
            chilog("Y: " + str(self.y) + " X: " + str(self.x))

        elif (c == ord('z')): #Placeing mode 
            self.action = "PLACE"
        
        elif (c == ord('x')):
            self.action = "BREAK"

        elif (c == ord('c')):
            self.action = "INTERACT"

        # Movement 
        elif (c in [ord(s) for s in ['d', 'a', 'w', 's']]):
            dir_tuple = dir[chr(c)]
            if (self.move_legal(dir_tuple, world) or debug):
                self.x += dir_tuple[1]
                self.y += dir_tuple[2]
            
        # Block action
        elif (c in [ord(s) for s in ['i', 'j', 'k', 'l']]):
            dir_tuple = dir[chr(c)]
            if (self.action == "PLACE"):
                if (self.place_legal(dir_tuple, world)):
                    ret = self.place_block(dir_tuple, world, stdscr, game)
            if (self.action == "BREAK"):
                self.break_block(dir_tuple, world, stdscr)
            if (self.action == "INTERACT"):
                self.interact_block(dir_tuple, world, stdscr, game.computers)

        # Inventory 
        elif (c in [ord(n) for n in items.keys()]):
            self.item = items[chr(c)]

        return ret
        

    # Movement Legality     
    def move_legal(self, dir_tuple, world):
        new_x = (self.x + dir_tuple[1]) % world.max_x
        blocktype = world.get_block_from_pos(self.y + dir_tuple[2], new_x).blocktypestr

        if (blocktype == "WATER" or blocktype == "AIR" or "WIRE" in blocktype or blocktype == "WEEDS"):
            return True 
        else:
            return False 


    # Block placement legality 
    def place_legal(self, dir_tuple, world):
        new_x = (self.x + dir_tuple[1]) % world.max_x
        blocktype = world.get_block_from_pos(self.y + dir_tuple[2], new_x).blocktypestr

        if (blocktype == "WATER" or blocktype == "AIR" or blocktype == "WEEDS"):
            return True 
        else:
            return False 

            
    # Block placement
    def place_block(self, dir_tuple, world, stdscr, game):
        new_x = (self.x + dir_tuple[1]) % world.max_x
        new_y = self.y + dir_tuple[2]
        b = blocks.Block(self.item, stdscr, new_y, new_x)
        world.map[new_y][new_x] = b

        if b.blocktypestr == "COMP":
            c = computer.Computer(b)
            game.computers.append(c)
            return 1

        elif "WIRE" in b.blocktypestr:
            return 1

        return 0

    def break_block(self, dir_tuple, world, stdscr):
        new_x = (self.x + dir_tuple[1]) % world.max_x
        if (world.map[self.y + dir_tuple[2]][new_x].blocktypestr == "BEDROCK"):
            return 

        world.map[self.y + dir_tuple[2]][new_x] = blocks.Block("AIR", stdscr, self.y + dir_tuple[2], new_x)
        world.coalesce_water(self.y + dir_tuple[2], new_x)
        world.map[self.y + dir_tuple[2]][self.x + dir_tuple[1]] = blocks.Block("AIR", stdscr, self.y + dir_tuple[2], self.x + dir_tuple[1])
        world.coalesce_water(self.y + dir_tuple[2], self.x + dir_tuple[1])

    
    # Block interaction 
    def interact_block(self, dir_tuple, world, stdscr, computers):
        """
        Check block type

        COMP - locate computer 

        ELSE - DO NOTHING
        """
        new_x = (self.x + dir_tuple[1]) % world.max_x
        blocktype = world.get_block_from_pos(self.y + dir_tuple[2], new_x).blocktypestr

        if (blocktype == "COMP"):
            cpu = computer.Computer.find_computer(computers, self.y + dir_tuple[2], new_x)

            if cpu.name == None:
                cpu.new_computer_prompt(stdscr)
            
            cpu.editor(stdscr)
            cpu.run()
        if (blocktype == "TNT"):
            # Set nearby blocks to be air, if that block happens to also be TNT, do the same 
            # with the exception that we're on the same block 
            """
               XXXXX
               XXTXX
               XXXXX 
            """
            # (y, x)
            self.blow_up(world, stdscr, self.y, self.x)

            
    
    def blow_up(self, world, stdscr, y, x):
        destroy_list = [(0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2)]
        for (dy, dx) in destroy_list:
            new_y = y + dy 
            new_x = (x + dx) % world.max_x
            if (new_y >= world.max_y):
                continue
            existing_block_type = world.map[new_y][new_x].blocktypestr
            if (existing_block_type == "TNT" and (dy, dx) != (0, 0)):
                self.blow_up(world, stdscr, new_y, new_x)
            world.map[new_y][new_x] = blocks.Block("AIR", stdscr, new_y, new_x)

