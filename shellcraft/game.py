import curses
from . import player, world
import time

class Game:

    def __init__(self):
        self.window = None
        self.player = player.Player()
        self.world = None

    def render(self):
        h, w = self.stdscr.getmaxyx()
        p_y, p_x = player.coords()

        y_min = max(0, p_y - (p_y // 2))
        y_max = min(h, p_y + (p_y // 2))
        x_min = max(0, p_y - (p_x // 2))
        x_max = min(w, p_x + (p_x // 2))

        for y in range(y_min, y_max + 1, 3):
            for x in range(x_min, x_max + 1, 3):
                self.world.draw(y, x)

    # The main game loop, use run() instead
    def __main(self, stdscr):
        self.stdscr = stdscr
        self.window = curses.initscr()

        self.stdscr.nodelay(True)
        self.stdscr.clear()
        curses.curs_set(0)

        self.world = world.World(self.stdscr)

        while (True):
            c = stdscr.getch()

            # Handle input here
            # Draw the new game here

            self.render()

            self.window.refresh()
            time.sleep(0.1)

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)
