import curses
from . import blocks, computer, player, world
import time
import copy

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

        
        screen_start = (max(p_y  - h // 2, 0 ), (p_x)  - w // 2)
                

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
        

        comp = computer.Computer("hello", blocks.Block("COMP", self.stdscr))

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
            time.sleep(.05)

    # Actually runs the game
    def run(self):
        curses.wrapper(self.__main)

    def handle_player_move(self, c):
        """
        Swap blocks
        """
        if (c == ord('d')): # Move Right
            self.player.x += 5
        if (c == ord('a')): # Move Left
            self.player.x -= 5
        if (c == ord('w')): 
            self.player.y -= 3
        if (c==ord('s')):
            self.player.y += 3

    def render_player(self):
        h, w = self.stdscr.getmaxyx()
        playerblock = blocks.Block("PLAYER", self.stdscr, self.player.y * 3, self.player.x)
        playerblock.draw((h - 3) // 2, (w - 5) // 2)

        # playerblock.draw(self.player.y * 3, self.player.x)
            
