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
                    Pixel(" ", 16, 233, 1), 
                    Pixel(" ", 16, 239, 2),
                    Pixel(" ", 16, 241, 3),
                    Pixel(" ", 16, 239, 4),
                    Pixel(" ", 16, 235, 5),

                ], 
                [
                    Pixel(" ", 16, 239, 6),
                    Pixel(" ", 16, 239, 7),
                    Pixel(" ", 16, 244, 8),
                    Pixel(" ", 16, 245, 9),
                    Pixel(" ", 16, 239, 10),

                ],
                [
                    Pixel(" ", 16, 232, 11),
                    Pixel(" ", 16, 233, 12),
                    Pixel(" ", 16, 239, 13),
                    Pixel(" ", 16, 239, 14),
                    Pixel(" ", 16, 247, 15),
                ]
            ],
            "DIRT": [[Pixel("X", curses.COLOR_GREEN, curses.COLOR_BLACK, 16)]],
            "CLOUD": [
                [
                    Pixel(" ", 16, 0, 31), 
                    Pixel(" ", 16, 240, 32),
                    Pixel(" ", 16, 255, 33),
                    Pixel(" ", 16, 247, 34),
                    Pixel(" ", 16, 0, 35),

                ], 
                [
                    Pixel(" ", 16, 0, 36),
                    Pixel(" ", 16, 255, 37),
                    Pixel(" ", 16, 246, 38),
                    Pixel(" ", 16, 255, 39),
                    Pixel(" ", 16, 0, 40),

                ],
                [
                    Pixel(" ", 16, 255, 41),
                    Pixel(" ", 16, 255, 42),
                    Pixel(" ", 16, 255, 43),
                    Pixel(" ", 16, 255, 44),
                    Pixel(" ", 16, 255, 45),
                ]
            ]
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
    def __init__(self, blocktype, screen): 
        self.blocktype = BType(blocktype)
        self.screen = screen

    def draw(self, locY, locX):
        """
        This function draws out a particular block given screen location
        * y+1
        """
        # print('=========' )
        # curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
        for i in range(3):
            for j in range(5):
                self.screen.addstr(locY + i, locX + j, self.blocktype.blocks[i][j].char, self.blocktype.blocks[i][j].colorpair)
        


        # self.screen.addstr(self.locX, self.locY, str(self.blocktype.blocks), curses.color_pair(9))