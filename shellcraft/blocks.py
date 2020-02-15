import curses
from enum import Enum 
from . pixel import Pixel

class BType(): 
    """
    3 by 3 array of pixels
    """


    def __init__(self, blocktype):
        blocklist = {
            "STONE": [
                [
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 1), 
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 2),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 3),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 4),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 4),

                ], 
                [
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 5),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 6),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 7),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 8),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 4),

                ],
                [
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 9),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 10),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 11),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 12),
                    Pixel("X", curses.COLOR_BLACK, curses.COLOR_WHITE, 4),

                ]
                ],
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
    def __init__(self, blocktype, screen, locY, locX): 
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
        # curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
        for i in range(3):
            for j in range(5):
                self.screen.addstr(self.locY + i, self.locX + j, self.blocktype.blocks[i][j].char, self.blocktype.blocks[i][j].colorpair)
        


        # self.screen.addstr(self.locX, self.locY, str(self.blocktype.blocks), curses.color_pair(9))