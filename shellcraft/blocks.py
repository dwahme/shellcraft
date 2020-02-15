import curses
from enum import Enum 
from . pixel import Pixel

class BType(): 
    """
    3 by 3 array of pixels
    """


    def __init__(self, blocktype):
        blocklist = {
            "STONE": [[Pixel("X", curses.COLOR_WHITE, curses.COLOR_RED, 1)]],
            "DIRT": [[Pixel("X", curses.COLOR_GREEN, curses.COLOR_BLACK, 10)]]
        }
        self.blocks = blocklist[blocktype]


    # CLOUD = [[]]
    # DIRT = [[]]
    # DIRTGRASS = [[]]
    # WATER = [[]]
    # SAND = [[]]
    # COMP = [[]]
    # WIRE = [[]]
    # AIR = [[]]


class Block:
    """
    This class generates a 3x3 block, given a type
    """
    def __init__(self, blocktype, screen, locX, locY): 
        self.blocktype = BType(blocktype)
        self.screen = screen
        self.locX = locX
        self.locY = locY

    def draw(self):
        """
        This function draws out a particular block given screen location
        * y+1
        """
        # print('=========' )
        curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
        self.screen.addstr(self.locX, self.locY, self.blocktype.blocks[0][0].char, self.blocktype.blocks[0][0].colorpair)
        # self.screen.addstr(self.locX, self.locY, str(self.blocktype.blocks), curses.color_pair(9))