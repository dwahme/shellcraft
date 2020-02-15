import curses
import time


class Game:

    def __init__(self):
        self.window = None
        self.map = []

    def render(self):
        h, w = stdscr.getmaxyx()

    # The main game loop, use run() instead
    def __main(self, stdscr):
        self.stdscr = stdscr
        self.window = curses.initscr()

        self.stdscr.nodelay(True)
        self.stdscr.clear()
        curses.curs_set(0)

        while (True):
            c = stdscr.getch()

            # Handle input here
            # Draw the new game here

            self.window.refresh()
            time.sleep(0.1)

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)
