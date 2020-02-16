import curses
from . import blocks, computer, player, world
import time
import copy
import math
from .enums.direction import Direction
from .utils.chilog import chilog

class Game:

    def __init__(self):
        self.player = player.Player()
        self.world = None
        self.stdscr = None
        self.computers = []

    def render_world(self):
        h, w = self.stdscr.getmaxyx()

        p_y, p_x = self.player.coords()
        p_y *= 3
        p_x *= 5
        
        screen_start = (p_y - h // 2, (p_x) - w // 2)

        for y in range(0, h - 2, 3):
            for x in range(0, w - 5, 5):
                ret = self.world.draw(y, x, (screen_start[0] + y) // 3, (screen_start[1] + x) // 5)

    player_block_type = {
        "NORMAL": "PLAYERNORMAL",
        "INTERACT": "PLAYERINTERACT",
        "PLACE": "PLAYERPLACE",
        "BREAK": "PLAYERBREAK"
    }

    def render_player(self):
        h, w = self.stdscr.getmaxyx()
        
        playerblock = blocks.Block(self.player_block_type[self.player.action], self.stdscr, self.player.y, self.player.x)
        playerblock.draw(self.roundbase(h // 2, 3), self.roundbase(w, 10) // 2) # magic, dont touch

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

            network_change = self.player.handle_player_move(c, self.world, self.stdscr, self)

            self.render_world()
            self.render_player()

            if network_change:
                chilog("\n")
                for c in self.computers:
                    c.update_network(self.world, self.computers)
                    chilog("{}\n".format(c.port_table))

            for c in self.computers:
                c.broadcast_all()

            self.stdscr.refresh()
            time.sleep(.01)

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)

    
    
    # UTILITY 
    def roundbase(self, x, base):
        # return int(math.ceil(x / 10.0)) * 10
        return base * round(x/base)
