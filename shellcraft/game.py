import curses


class Game:

    def __init__(self):
        self.stdscr = None

    # The main game loop, use run() instead
    def __main(self, stdscr):
        self.stdscr = stdscr

        self.stdscr.nodelay(True)
        self.stdscr.clear()

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)
