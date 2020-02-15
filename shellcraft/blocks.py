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
        self.screen.addstr(self.locY, self.locX, self.blocktype.blocks[0][0].char, self.blocktype.blocks[0][0].colorpair)
        self.screen.addstr(self.locY, self.locX + 1, self.blocktype.blocks[0][1].char, self.blocktype.blocks[0][1].colorpair)
        self.screen.addstr(self.locY, self.locX + 2, self.blocktype.blocks[0][2].char, self.blocktype.blocks[0][2].colorpair)
        self.screen.addstr(self.locY, self.locX + 3, self.blocktype.blocks[0][3].char, self.blocktype.blocks[0][3].colorpair)
        self.screen.addstr(self.locY, self.locX + 4, self.blocktype.blocks[0][4].char, self.blocktype.blocks[0][4].colorpair)


        self.screen.addstr(self.locY + 1, self.locX, self.blocktype.blocks[1][0].char, self.blocktype.blocks[1][0].colorpair)
        self.screen.addstr(self.locY + 1, self.locX + 1, self.blocktype.blocks[1][1].char, self.blocktype.blocks[1][1].colorpair)
        self.screen.addstr(self.locY + 1, self.locX + 2, self.blocktype.blocks[1][2].char, self.blocktype.blocks[1][2].colorpair)
        self.screen.addstr(self.locY + 1, self.locX + 3, self.blocktype.blocks[1][3].char, self.blocktype.blocks[1][3].colorpair)
        self.screen.addstr(self.locY + 1, self.locX + 4, self.blocktype.blocks[1][4].char, self.blocktype.blocks[1][4].colorpair)


        self.screen.addstr(self.locY + 2, self.locX, self.blocktype.blocks[2][0].char, self.blocktype.blocks[2][0].colorpair)
        self.screen.addstr(self.locY + 2, self.locX + 1, self.blocktype.blocks[2][1].char, self.blocktype.blocks[2][1].colorpair)
        self.screen.addstr(self.locY + 2, self.locX + 2, self.blocktype.blocks[2][2].char, self.blocktype.blocks[2][2].colorpair)
        self.screen.addstr(self.locY + 2, self.locX + 3, self.blocktype.blocks[2][3].char, self.blocktype.blocks[2][3].colorpair)
        self.screen.addstr(self.locY + 2, self.locX + 4, self.blocktype.blocks[1][4].char, self.blocktype.blocks[1][4].colorpair)
        


        # self.screen.addstr(self.locX, self.locY, str(self.blocktype.blocks), curses.color_pair(9))