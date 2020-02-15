import curses
from . import computer, player, world
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

        screen_start = (p_y * 3 - h // 2, p_x * 5 - w // 2)

        for y in range(0, h - 2, 3):
            for x in range(0, w - 4, 5):
                ret = self.world.draw(y, x, (screen_start[0] + y) // 3, (screen_start[1] + x) // 5)

    # The main game loop, use run() instead
    def __main(self, stdscr):
        self.stdscr = stdscr

        self.stdscr.nodelay(True)
        self.stdscr.clear()
        curses.curs_set(0)

        self.world = world.World(self.stdscr)
        self.world.generate()

        comp = computer.Computer("hello")

        while (True):
            c = stdscr.getch()

            # Handle input here
            # TODO- yves: based upon the character that's inputted, do update player y/x
            # or get some other input here and handle
            # preferably some dispatch function?
            # NOTE THAT PLAYER Y VALUE DOES NOT WRAP (BUT X DOES)

            if c == 101:
                comp.editor(self.stdscr)

            else:
                self.render()

            time.sleep(2)

            if comp.process != None:
                print(comp.read_pipe())

            self.stdscr.refresh()

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)
