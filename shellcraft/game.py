import curses
from . import blocks, computer, monitor, player, world
import time
import copy
import math
import os
from pathlib import Path
from .enums.direction import Direction
from .enums.event import Event
from .utils.chilog import chilog

class Game:

    def __init__(self, editor):
        self.player = player.Player()
        self.world = None
        self.stdscr = None
        self.computers = []
        self.monitors = []

        # Set the default editor
        computer.Computer.EDITOR = editor

    def coord_convert(self, y, x):
        h, w = self.stdscr.getmaxyx()

        p_y, p_x = self.player.coords()
        p_y *= 3
        p_x *= 5
        
        screen_start = (p_y - h // 2, (p_x) - w // 2)

        return (screen_start[0] + y) // 3, ((screen_start[1] + x) // 5) % self.world.max_x


    def render_world(self):
        h, w = self.stdscr.getmaxyx()

        for y in range(0, h - 2, 3):
            for x in range(0, w - 5, 5):
                new_y, new_x = self.coord_convert(y, x)
                drawn = False

                for m in self.monitors:
                    if m.in_bounds(new_y, new_x) and m.is_rectangle():
                        if (new_y, new_x) == m.blocks[0].coords():
                            m.render(self.stdscr, y, x)
                        drawn = True

                if not drawn:
                    self.world.draw(y, x, new_y, new_x)

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

        # i = 0

        while (True):
            # i += 1
            c = stdscr.getch()

            # Handle input here
            # TODO- yves: based upon the character that's inputted, do update player y/x
            # or get some other input here and handle
            # preferably some dispatch function?
            # NOTE THAT PLAYER Y VALUE DOES NOT WRAP (BUT X DOES)

            event = self.player.handle_player_move(c, self.world, self.stdscr, self)

            self.render_world()
            self.render_player()


            if event == Event.MONITOR_CHANGE:
                self.monitors = monitor.Monitor.aggregate_monitors(self.monitors)

            if event == Event.COMPUTER_CHANGE or event == Event.MONITOR_CHANGE:
                iomonitors = [io for m in self.monitors for io in m.generate_iomonitors()]
                chilog("TOTALIO: {}".format(iomonitors))

                for c in self.computers:
                    c.update_network(self.world, self.computers + iomonitors)

            for c in self.computers:
                c.broadcast_all()

            self.stdscr.refresh()
            time.sleep(.01)

    # Actually runs the game
    def run(self):
        # Prepare for logging and program files
        if os.path.exists("log.txt"):
            os.remove("log.txt")
        Path("./computer_files").mkdir(parents=True, exist_ok=True)

        # Run the game
        curses.wrapper(self.__main)
    
    
    # UTILITY 
    def roundbase(self, x, base):
        # return int(math.ceil(x / 10.0)) * 10
        return base * round(x/base)
