import curses
from . import blocks, computer, monitor, player, world
import time
import copy
import random
import math
import os
from pathlib import Path
from .enums.direction import Direction
from .enums.event import Event
from .utils.chilog import chilog

class Game:

    def __init__(self, editor, seed):
        self.player = player.Player()
        self.seed = seed
        self.world = None
        self.stdscr = None
        self.computers = []
        self.pis = []
        self.frame_count = 0
        # self.monsters = []
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
    
    def render_physics(self):
        # if the below block is water, slowly sink 
        bottomblock = self.world.get_block_from_pos(self.player.y + 1, self.player.x)
        if (bottomblock.blocktypestr == "WATER"):
            if (self.frame_count % 100 == 0):
                self.player.y += 1
        if (self.frame_count % 600 == 0):
            self.grow_weeds()
    
    def grow_weeds(self):
        # Grab bare dirtgrass blocks 
        # loop through x: 0-worldmax_x
        weed_pos = []
        for x in range(self.world.max_x):
            for y in range(3, self.world.ground + 1):
                block_type = self.world.map[y][x].blocktypestr
                if (block_type != "AIR"):
                    if (block_type == "DIRTGRASS"):
                        if (random.random() < 0.3):
                            weed_pos.append((y, x))
                    else: 
                        break
        chilog(str(weed_pos))
        for weed in weed_pos:
            self.world.map[weed[0] - 1][weed[1]] = blocks.Block("WEEDS", self.stdscr, weed[0] - 1, weed[1])

    # The main game loop, use run() instead
    def __main(self, stdscr):
        self.stdscr = stdscr

        self.stdscr.nodelay(True)
        self.stdscr.clear()
        curses.curs_set(0)

        self.world = world.World(self.stdscr, self.seed)
        self.world.generate()
        self.player.y, self.player.x = self.world.spawn()

        while (True):
            c = stdscr.getch()
            
            event = self.player.handle_player_move(c, self.world, self.stdscr, self)

            self.render_world()
            self.render_player()
            self.render_physics()


            if event == Event.MONITOR_CHANGE:
                self.monitors = monitor.Monitor.aggregate_monitors(self.monitors)

            if event == Event.COMPUTER_CHANGE or event == Event.MONITOR_CHANGE:
                iomonitors = [io for m in self.monitors for io in m.generate_iomonitors()]
                chilog("TOTALIO: {}".format(iomonitors))

                for c in self.computers:
                    c.update_network(self.world, self.computers + self.pis + iomonitors)

            for c in self.computers + self.pis:
                c.broadcast_all()

            self.stdscr.refresh()
            time.sleep(.01)
            self.frame_count = (self.frame_count + 1) % 3000

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
