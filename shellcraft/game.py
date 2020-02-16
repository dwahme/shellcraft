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
        return self.world.map[y][x % self.world.max_x] # wraping

    # The main game loop, use run() instead
    def __main(self, stdscr):
        self.stdscr = stdscr

        self.stdscr.nodelay(True)
        self.stdscr.clear()
        curses.curs_set(0)

        self.world = world.World(self.stdscr)
        self.world.generate()
        self.player.y, self.player.x = self.world.spawn()

        comp = computer.Computer("hello", blocks.Block("COMP", self.stdscr, 15, 250))

        while (True):
            c = stdscr.getch()

            # Handle input here
            # TODO- yves: based upon the character that's inputted, do update player y/x
            # or get some other input here and handle
            # preferably some dispatch function?
            # NOTE THAT PLAYER Y VALUE DOES NOT WRAP (BUT X DOES)

            self.handle_player_move(c)

            
            if c == 114: # r
                comp.run()
            if c == 101: # e
                comp.editor(self.stdscr)
            else:
                self.render_world()
                self.render_player()

            # if computer or wire block added/deleted
            for c in self.computers:
                c.update_network(self.world)

            if comp.process != None:
                print(comp.read_port(2))

            self.stdscr.refresh()
            time.sleep(.01)

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)

    def handle_player_move(self, c):
        """
        Swap blocks
        """

        # Debug
        debug = False

        if (c == ord(' ') and debug):
            chilog("Y: " + str(self.player.y) + " X: " + str(self.player.x))

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

        # Block placement
        elif (c == ord('l')): #Place block right
            if (self.place_right_legal()):
                self.place_block_right()


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


def chilog(msg):
    f = open("debug.txt", "w")
    f.write(msg)
    f.close()