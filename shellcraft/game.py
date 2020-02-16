import curses
from . import blocks, computer, player, world
import time
import copy
import math

class Game:

    def __init__(self):
        self.player = player.Player()
        self.world = None
        self.stdscr = None
        self.computers = []

    def render_world(self):
        h, w = self.stdscr.getmaxyx()

        p_y, p_x = self.player.coords()
        # p_x %= world.World.max_x
        # p_y %= world.World.max_y
        p_y *= 3
        p_x *= 5
        
        screen_start = (p_y - h // 2, (p_x) - w // 2)

        for y in range(0, h - 2, 3):
            for x in range(0, w - 5, 5):
                ret = self.world.draw(y, x, (screen_start[0] + y) // 3, (screen_start[1] + x) // 5)

    # def get_block_from_screen_pos(self, y, x):
    #     """
    #     y, x is the map's indexing of the various blocks, not the pixel coordinates
    #     """
    #     h, w = self.stdscr.getmaxyx()
    #     p_y, p_x = self.player.coords()
    #     p_y *= 3
    #     p_x *= 5
    #     screen_start = (p_y - h // 2, (p_x) - w // 2)
    #     block_y = (screen_start[0] + y) // 3
    #     block_x = (screen_start[1] + x) // 5
    #     block = self.world.map[block_y][block_x % self.world.max_x]

    #     return block

    def get_block_from_pos(self, y, x): 
        """
        y, x: index of block
        """
        return self.world.map[y][x % self.world.max_x] # wrapping

    # The main game loop, use run() instead
    def __main(self, stdscr):
        self.stdscr = stdscr

        self.stdscr.nodelay(True)
        self.stdscr.clear()
        curses.curs_set(0)

        self.world = world.World(self.stdscr)
        self.world.generate()
        self.player.y, self.player.x = self.world.spawn()

        while (True):
            c = stdscr.getch()

            # Handle input here
            # TODO- yves: based upon the character that's inputted, do update player y/x
            # or get some other input here and handle
            # preferably some dispatch function?
            # NOTE THAT PLAYER Y VALUE DOES NOT WRAP (BUT X DOES)

            # chilog("{}".format(self.player.coords()))

            self.handle_player_move(c)

            self.render_world()
            self.render_player()

            # if computer or wire block added/deleted
            for c in self.computers:
                c.update_network(self.world, self.computers)

            # for c in self.computers:
            #     c.broadcast_all()

            self.stdscr.refresh()
            time.sleep(.01)

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)

    def handle_player_move(self, c):
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
            chilog("Y: " + str(self.player.y) + " X: " + str(self.player.x))

        elif (c == ord('z')): #Placeing mode 
            self.player.action = "PLACE"
        
        elif (c == ord('x')):
            self.player.action = "BREAK"

        # Movement 
        elif (c == ord('d')): # Move Right
            if (self.move_right_legal() or debug):
                self.player.x += 1
        elif (c == ord('a')): # Move Left
            if (self.move_left_legal() or debug):
                self.player.x -= 1
        elif (c == ord('w')): # Move Up
            if (self.move_up_legal() or debug):
                self.player.y -= 1
        elif (c == ord('s')): #Move Down 
            if (self.move_down_legal() or debug):
                self.player.y += 1

        # Block action
        elif (c == ord('l')): #Place block right
            if (self.player.action == "PLACE"):
                if (self.place_right_legal()):
                    self.place_block_right()
            if (self.player.action == "BREAK"):
                self.break_block_right()

        elif (c == ord('j')): #Place block right
            if (self.player.action == "PLACE"):
                if (self.place_left_legal()):
                    self.place_block_left()
            if (self.player.action == "BREAK"):
                self.break_block_left()

        elif (c == ord('i')): #Place block right
            if (self.player.action == "PLACE"):
                if (self.place_up_legal()):
                    self.place_block_up()
            if (self.player.action == "BREAK"):
                self.break_block_up()

        elif (c == ord('k')): #Place block right
            if (self.player.action == "PLACE"):
                if (self.place_down_legal()):
                    self.place_block_down()
            if (self.player.action == "BREAK"):
                self.break_block_down()

        # Inventory 
        elif (c == ord('1')): # Inventory 1
            self.player.item = "DIRT"
        elif (c == ord('2')): # Inventory 1
            self.player.item = "COMP"
        elif (c == ord('3')): # Inventory 1
            self.player.item = "WIRE_LRTB"
        elif (c == ord('4')): # Inventory 2
            self.player.item = "STONE"

    def render_player(self):
        h, w = self.stdscr.getmaxyx()
        playerblock = blocks.Block("PLAYER", self.stdscr, self.player.y, self.player.x)
        playerblock.draw(self.roundbase(h // 2, 3), self.roundbase(w, 10) // 2) # magic, dont touch

    def roundbase(self, x, base):
        # return int(math.ceil(x / 10.0)) * 10
        return base * round(x/base)


    # Movement Legality 
    def move_down_legal(self):
        # Checks what's below the player 
        block_below = self.get_block_from_pos(self.player.y + 1, self.player.x)

        if (block_below.blocktypestr == "WATER" or block_below.blocktypestr == "AIR"):
            return True
        else:
            return False

    def move_right_legal(self):
        block_right_type = self.get_block_from_pos(self.player.y, self.player.x + 1).blocktypestr
        if (block_right_type == "WATER" or block_right_type == "AIR"):
            return True
        else:
            return False

    def move_left_legal(self):
        block_left_type = self.get_block_from_pos(self.player.y, self.player.x - 1).blocktypestr
        if (block_left_type == "WATER" or block_left_type == "AIR"):
            return True
        else:
            return False

    def move_up_legal(self):
        block_up_type = self.get_block_from_pos(self.player.y - 1, self.player.x).blocktypestr
        if (block_up_type == "WATER" or block_up_type == "AIR"):
            return True
        else:
            return False


    # Block placement legality 
    def place_right_legal(self): 
        block_type = self.get_block_from_pos(self.player.y, self.player.x + 1).blocktypestr
        if (block_type == "AIR" or block_type == "WATER"):
            return True
        else:
            return False

    def place_left_legal(self): 
        block_type = self.get_block_from_pos(self.player.y, self.player.x - 1).blocktypestr
        if (block_type == "AIR" or block_type == "WATER"):
            return True
        else:
            return False

    def place_up_legal(self): 
        block_type = self.get_block_from_pos(self.player.y - 1, self.player.x).blocktypestr
        if (block_type == "AIR" or block_type == "WATER"):
            return True
        else:
            return False

    def place_down_legal(self): 
        block_type = self.get_block_from_pos(self.player.y + 1, self.player.x + 1).blocktypestr
        if (block_type == "AIR" or block_type == "WATER"):
            return True
        else:
            return False


    # Block placement functionality 
    def place_block_right(self): 
        b = blocks.Block(self.player.item, self.stdscr, self.player.y, self.player.x + 1)
        chilog("block coords = {}".format(b.coords()))
        self.world.map[self.player.y][self.player.x + 1] = b
        if self.player.item == "COMP":
            c = computer.Computer(str(len(self.computers)), b)
            self.computers.append(c)
            c.editor(self.stdscr)

    def place_block_left(self): 
        b = blocks.Block(self.player.item, self.stdscr, self.player.y, self.player.x - 1)
        chilog("block coords = {}".format(b.coords()))
        self.world.map[self.player.y][self.player.x - 1] = b
        if self.player.item == "COMP":
            c = computer.Computer(str(len(self.computers)), b)
            self.computers.append(c)
            c.editor(self.stdscr)

    def place_block_up(self): 
        b = blocks.Block(self.player.item, self.stdscr, self.player.y - 1, self.player.x)
        chilog("block coords = {}".format(b.coords()))
        self.world.map[self.player.y - 1][self.player.x] = b
        if self.player.item == "COMP":
            c = computer.Computer(str(len(self.computers)), b)
            self.computers.append(c)
            c.editor(self.stdscr)

    def place_block_down(self): 
        b = blocks.Block(self.player.item, self.stdscr, self.player.y + 1, self.player.x)
        chilog("block coords = {}".format(b.coords()))
        self.world.map[self.player.y + 1][self.player.x] = b
        if self.player.item == "COMP":
            c = computer.Computer(str(len(self.computers)), b)
            self.computers.append(c)
            c.editor(self.stdscr)


    # Block deletion functionality 
    def break_block_right(self):
        self.world.map[self.player.y][self.player.x + 1] = blocks.Block("AIR", self.stdscr, self.player.y, self.player.x + 1)

    def break_block_left(self):
        self.world.map[self.player.y][self.player.x - 1] = blocks.Block("AIR", self.stdscr, self.player.y, self.player.x - 1)

    def break_block_up(self):
        self.world.map[self.player.y - 1][self.player.x] = blocks.Block("AIR", self.stdscr, self.player.y - 1, self.player.x)

    def break_block_down(self):
        self.world.map[self.player.y + 1][self.player.x] = blocks.Block("AIR", self.stdscr, self.player.y + 1, self.player.x)
    

def chilog(msg):
    f = open("debug.txt", "a+")
    f.write(msg)
    f.close()