import curses
import sys
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
                    Pixel(" ", 16, 238, 15),
                ]
            ],
            "DIRT": [[Pixel("X", curses.COLOR_GREEN, curses.COLOR_BLACK, 16)]],
            "CLOUD": [
                [
                    Pixel(" ", 16, 0, 31), 
                    Pixel(" ", 16, 240, 32),
                    Pixel(" ", 16, 249, 33),
                    Pixel(" ", 16, 247, 34),
                    Pixel(" ", 16, 0, 35),

                ], 
                [
                    Pixel(" ", 16, 0, 36),
                    Pixel(" ", 16, 249, 37),
                    Pixel(" ", 16, 246, 38),
                    Pixel(" ", 16, 251, 39),
                    Pixel(" ", 16, 0, 40),

                ],
                [
                    Pixel(" ", 16, 249, 41),
                    Pixel(" ", 16, 250, 42),
                    Pixel(" ", 16, 251, 43),
                    Pixel(" ", 16, 250, 44),
                    Pixel(" ", 16, 249, 45),
                ]
            ],
            "WATER": [
                [
                    Pixel(" ", 16, 27, 46), 
                    Pixel(" ", 16, 33, 47),
                    Pixel(" ", 16, 27, 48),
                    Pixel(" ", 16, 32, 49),
                    Pixel(" ", 16, 27, 50),

                ], 
                [
                    Pixel(" ", 16, 27, 51),
                    Pixel(" ", 16, 27, 52),
                    Pixel(" ", 16, 33, 53),
                    Pixel(" ", 16, 27, 54),
                    Pixel(" ", 16, 32, 55),

                ],
                [
                    Pixel(" ", 16, 33, 56),
                    Pixel(" ", 16, 27, 57),
                    Pixel(" ", 16, 32, 58),
                    Pixel(" ", 16, 33, 59),
                    Pixel(" ", 16, 26, 60),
                ]
            ],
            "COMP": [
                [
                    Pixel("#", 16, 254, 76), 
                    Pixel(" ", 16, 16, 77),
                    Pixel(" ", 16, 16, 78),
                    Pixel(" ", 16, 254, 79),
                    Pixel("#", 16, 254, 80),

                ], 
                [
                    Pixel(" ", 16, 254, 81),
                    Pixel(" ", 16, 254, 82),
                    Pixel(" ", 16, 254, 83),
                    Pixel(" ", 16, 16, 84),
                    Pixel(" ", 16, 16, 85),

                ],
                [
                    Pixel("#", 16, 254, 86),
                    Pixel(" ", 16, 16, 87),
                    Pixel(" ", 16, 16, 88),
                    Pixel(" ", 16, 254, 89),
                    Pixel("#", 16, 254, 90),
                ]
            ]
        }
        self.blocks = blocklist[blocktype]


    # SAND = [[]] 91-105
    # COMP = [[]]
    # WIRE = [[]]
    # AIR = [[]]


class Block:
    """
    This class generates a 3x3 block, given a type

    example:
    b = Block("STONE", self.stdscr)

    """
    def __init__(self, blocktype, screen): 
        self.blocktype = BType(blocktype)
        self.screen = screen

    def draw(self, locY, locX):
        """
        This function draws out a particular block given screen location
        
        e.g. b.draw(10, 5)
        """
        # print('=========' )
        # curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)
        for i in range(3):
            for j in range(5):
                self.screen.addstr(locY + i, locX + j, self.blocktype.blocks[i][j].char, self.blocktype.blocks[i][j].colorpair)
        


        # self.screen.addstr(self.locX, self.locY, str(self.blocktype.blocks), curses.color_pair(9))