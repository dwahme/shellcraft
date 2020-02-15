import curses
from . import player, world, blocks
import time

class Game:

    def __init__(self):
        self.player = player.Player()
        self.world = None
        self.stdscr = None

    def render(self):
        h, w = self.stdscr.getmaxyx()

        p_y, p_x = self.player.coords()
        p_x %= world.World.max_x

        
        screen_start = (max(p_y * 3 - h // 2, 0 ), p_x * 5 - w // 2)

        self.world.map[p_y][p_x] = blocks.Block("PLAYER", self.stdscr)

        for y in range(0, h - 2, 3):
            for x in range(0, w - 5, 5):
                ret = self.world.draw(y, x, (screen_start[0] + y) // 3 , (screen_start[1] + x) // 5)

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
            self.player.handleMovement(c)

            self.render()

            self.stdscr.refresh()
            time.sleep(.5)

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)
