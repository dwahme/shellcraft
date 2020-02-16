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
                    Pixel(" ", 16, 243, 1), 
                    Pixel(" ", 16, 241, 2),
                    Pixel(" ", 16, 241, 3),
                    Pixel(" ", 16, 243, 4),
                    Pixel(" ", 16, 239, 5),

                ], 
                [
                    Pixel(" ", 16, 241, 6),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 239, 8),
                    Pixel(" ", 16, 245, 9),
                    Pixel(" ", 16, 241, 10),

                ],
                [
                    Pixel(" ", 16, 241, 11),
                    Pixel(" ", 16, 239, 12),
                    Pixel(" ", 16, 245, 13),
                    Pixel(" ", 16, 243, 14),
                    Pixel(" ", 16, 243, 15),
                ]
            ],
            "DIRT": [
                [
                    Pixel(" ", 1, 100, 16),
                    Pixel(" ", 1, 94, 17),
                    Pixel(" ", 1, 94, 18),
                    Pixel(" ", 1, 100, 19),
                    Pixel(" ", 1, 136, 20)
                ],
                [
                    Pixel(" ", 1, 94, 21),
                    Pixel(" ", 1, 136, 22),
                    Pixel(" ", 1, 94, 23),
                    Pixel(" ", 1, 100, 24),
                    Pixel(" ", 1, 94, 25)
                ],
                [
                    Pixel(" ", 1, 136, 26),
                    Pixel(" ", 1, 100, 27),
                    Pixel(" ", 1, 136, 28),
                    Pixel(" ", 1, 94, 29),
                    Pixel(" ", 1, 94, 30)
                ]
            ],
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
            "DIRTGRASS": [
                [
                    Pixel("\"", 10, 28, 61),
                    Pixel(" ", 1, 22, 62),
                    Pixel(" ", 1, 28, 63),
                    Pixel("§", 28, 22, 64),
                    Pixel(" ", 1, 22, 65)
                ],
                [
                    Pixel("§", 28, 10, 66),
                    Pixel(" ", 1, 28, 67),
                    Pixel("\'", 10, 28, 68),
                    Pixel("\"", 10, 22, 69),
                    Pixel(" ", 1, 28, 70)
                ],
                [
                    Pixel(" ", 1, 28, 71),
                    Pixel("§", 28, 10, 72),
                    Pixel("§", 22, 10, 73),
                    Pixel(" ", 1, 28, 74),
                    Pixel("\"", 10, 22, 75)
                ]
            ],
            "COMP": [
                [
                    Pixel("-", 16, 253, 76), 
                    Pixel("-", 16, 253, 77),
                    Pixel("-", 16, 253, 78),
                    Pixel("-", 16, 253, 79),
                    Pixel("-", 16, 253, 80),

                ], 
                [
                    Pixel("¦", 16, 253, 81),
                    Pixel("'", 16, 245, 82),
                    Pixel("v", 16, 245, 83),
                    Pixel("'", 16, 245, 84),
                    Pixel("¦", 16, 253, 85),

                ],
                [
                    Pixel("-", 16, 253, 86),
                    Pixel("-", 16, 253, 87),
                    Pixel("-", 16, 253, 88),
                    Pixel("-", 16, 253, 89),
                    Pixel("-", 16, 253, 90),
                ]
            ],
            "SAND": [
                [
                    Pixel(" ", 1, 220, 91),
                    Pixel(" ", 1, 222, 92),
                    Pixel(" ", 1, 221, 93),
                    Pixel(" ", 1, 220, 94),
                    Pixel(" ", 1, 220, 95)
                ],
                [
                    Pixel(" ", 1, 221, 96),
                    Pixel(" ", 1, 222, 97),
                    Pixel(" ", 1, 220, 98),
                    Pixel(" ", 1, 220, 99),
                    Pixel(" ", 1, 221, 100),
                ],
                [
                    Pixel(" ", 1, 222, 101),
                    Pixel(" ", 1, 220, 102),
                    Pixel(" ", 1, 221, 103),
                    Pixel(" ", 1, 221, 104),
                    Pixel(" ", 1, 220, 105)
                ]
            ],
            "AIR": [
                [
                    Pixel(" ", 16, 0, 106), 
                    Pixel(" ", 16, 0, 107),
                    Pixel(" ", 16, 0, 108),
                    Pixel(" ", 16, 0, 109),
                    Pixel(" ", 16, 0, 110),

                ], 
                [
                    Pixel(" ", 16, 0, 111),
                    Pixel(" ", 16, 0, 112),
                    Pixel(" ", 16, 0, 113),
                    Pixel(" ", 16, 0, 114),
                    Pixel(" ", 16, 0, 115),

                ],
                [
                    Pixel(" ", 16, 0, 116),
                    Pixel(" ", 16, 0, 117),
                    Pixel(" ", 16, 0, 118),
                    Pixel(" ", 16, 0, 119),
                    Pixel(" ", 16, 0, 120),
                ]
            ],
            "WIRE_LR" : [
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ],
                [
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                ],
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_LT" : [
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel("#", 255, 1, 122),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ],
                [
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ],
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_LB" : [
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ],
                [
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ],
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel("#", 255, 1, 122),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_RT" : [
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel("#", 255, 1, 122),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ],
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                ],
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_RB" : [
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ],
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                    Pixel("#", 255, 1, 122),
                ],
                [
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                    Pixel("#", 255, 1, 122),
                    Pixel(" ", 255, 0, 121),
                    Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_TB" : [
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ],
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ],
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_LRT" : [
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ],
                [
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                ],
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_LRB" : [
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ],
                [
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                ],
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_LTB" : [
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ],
                [
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ],
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_RTB" : [
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ],
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                ],
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ]
            ],
            "WIRE_LRTB" : [
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ],
                [
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                Pixel("#", 255, 1, 122),
                ],
                [
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                Pixel("#", 255, 1, 122),
                Pixel(" ", 255, 0, 121),
                Pixel(" ", 255, 0, 121),
                ]
            ],
            "FRAME" : [
                [
                Pixel(">", 255, 0, 123),
                Pixel("-", 255, 0, 123),
                Pixel("-", 255, 1, 123),
                Pixel("-", 255, 0, 123),
                Pixel("<", 255, 0, 123),
                ],
                [
                Pixel("|", 255, 1, 123),
                Pixel(" ", 255, 1, 123),
                Pixel("*", 255, 1, 123),
                Pixel(" ", 255, 1, 123),
                Pixel("|", 255, 1, 123),
                ],
                [
                Pixel(">", 255, 0, 123),
                Pixel("-", 255, 0, 123),
                Pixel("-", 255, 1, 123),
                Pixel("-", 255, 0, 123),
                Pixel("<", 255, 0, 123),
                ]
            ],
            "PLAYER": [
                [
                    Pixel("^", 16, 212, 136), 
                    Pixel(" ", 16, 212, 137),
                    Pixel(" ", 16, 212, 138),
                    Pixel(" ", 16, 212, 139),
                    Pixel("^", 16, 212, 140),

                ], 
                [
                    Pixel(" ", 16, 212, 141),
                    Pixel("u", 16, 212, 142),
                    Pixel("w", 16, 212, 143),
                    Pixel("u", 16, 212, 144),
                    Pixel(" ", 16, 212, 145),

                ],
                [
                    Pixel(" ", 16, 212, 146),
                    Pixel(" ", 16, 212, 147),
                    Pixel(" ", 16, 212, 148),
                    Pixel(" ", 16, 212, 149),
                    Pixel(" ", 16, 212, 150),
                ]
            ],
            "BEDROCK": [
                [
                    Pixel(" ", 16, 233, 151), 
                    Pixel(" ", 16, 239, 152),
                    Pixel(" ", 16, 241, 153),
                    Pixel(" ", 16, 239, 154),
                    Pixel(" ", 16, 235, 155),

                ], 
                [
                    Pixel(" ", 16, 239, 156),
                    Pixel(" ", 16, 239, 157),
                    Pixel(" ", 16, 244, 158),
                    Pixel(" ", 16, 245, 159),
                    Pixel(" ", 16, 239, 160),

                ],
                [
                    Pixel(" ", 16, 232, 161),
                    Pixel(" ", 16, 233, 162),
                    Pixel(" ", 16, 239, 163),
                    Pixel(" ", 16, 239, 164),
                    Pixel(" ", 16, 238, 165),
                ]
            ],
            "ZEROZERO": [
                [
                    Pixel(" ", 16, 212, 136), 
                    Pixel(" ", 16, 212, 137),
                    Pixel(" ", 16, 212, 138),
                    Pixel(" ", 16, 212, 139),
                    Pixel(" ", 16, 212, 140),

                ], 
                [
                    Pixel(" ", 16, 212, 141),
                    Pixel("0", 16, 212, 142),
                    Pixel(",", 16, 212, 143),
                    Pixel("0", 16, 212, 144),
                    Pixel(" ", 16, 212, 145),

                ],
                [
                    Pixel(" ", 16, 212, 146),
                    Pixel(" ", 16, 212, 147),
                    Pixel(" ", 16, 212, 148),
                    Pixel(" ", 16, 212, 149),
                    Pixel(" ", 16, 212, 150),
                ]
            ],
            "ZEROONE": [
                [
                    Pixel(" ", 16, 212, 136), 
                    Pixel(" ", 16, 212, 137),
                    Pixel(" ", 16, 212, 138),
                    Pixel(" ", 16, 212, 139),
                    Pixel(" ", 16, 212, 140),

                ], 
                [
                    Pixel(" ", 16, 212, 141),
                    Pixel("0", 16, 212, 142),
                    Pixel(",", 16, 212, 143),
                    Pixel("1", 16, 212, 144),
                    Pixel(" ", 16, 212, 145),

                ],
                [
                    Pixel(" ", 16, 212, 146),
                    Pixel(" ", 16, 212, 147),
                    Pixel(" ", 16, 212, 148),
                    Pixel(" ", 16, 212, 149),
                    Pixel(" ", 16, 212, 150),
                ]
            ],
            "ONEZERO": [
                [
                    Pixel(" ", 16, 212, 136), 
                    Pixel(" ", 16, 212, 137),
                    Pixel(" ", 16, 212, 138),
                    Pixel(" ", 16, 212, 139),
                    Pixel(" ", 16, 212, 140),

                ], 
                [
                    Pixel(" ", 16, 212, 141),
                    Pixel("1", 16, 212, 142),
                    Pixel(",", 16, 212, 143),
                    Pixel("0", 16, 212, 144),
                    Pixel(" ", 16, 212, 145),

                ],
                [
                    Pixel(" ", 16, 212, 146),
                    Pixel(" ", 16, 212, 147),
                    Pixel(" ", 16, 212, 148),
                    Pixel(" ", 16, 212, 149),
                    Pixel(" ", 16, 212, 150),
                ]
            ],
            "LAVA": [
                [
                    Pixel(" ", 16, 9, 151), 
                    Pixel(" ", 16, 196, 152),
                    Pixel(" ", 16, 9, 153),
                    Pixel(" ", 16, 196, 154),
                    Pixel(" ", 16, 52, 155),

                ], 
                [
                    Pixel(" ", 16, 196, 156),
                    Pixel(" ", 16, 88, 157),
                    Pixel(" ", 16, 196, 158),
                    Pixel(" ", 16, 196, 159),
                    Pixel(" ", 16, 9, 160),

                ],
                [
                    Pixel(" ", 16, 52, 161),
                    Pixel(" ", 16, 196, 162),
                    Pixel(" ", 16, 124, 163),
                    Pixel(" ", 16, 52, 164),
                    Pixel(" ", 16, 88, 165),
                ]
            ],
        }
        self.blocks = blocklist[blocktype]


    # 121-165 
    # COMP = [[]]
    # WIRE = [[]]
    # AIR = [[]]


class Block:
    """
    This class generates a 3x3 block, given a type

    example:
    b = Block("STONE", self.stdscr)

    """
    def __init__(self, blocktype, screen, y, x): 
        self.blocktypestr = blocktype
        self.blocktype = BType(blocktype)
        self.screen = screen
        self.y = y # Map array Index
        self.x = x # Map array index

    def draw(self, locY, locX): #Screen coords
        """
        This function draws out a particular block given screen location
        
        e.g. b.draw(10, 5)
        """
        # print('=========' )
        # curses.init_pair(9, curses.COLOR_RED, curses.COLOR_WHITE)

        for i in range(3):
            for j in range(5):
                self.screen.addstr(locY + i, locX + j, self.blocktype.blocks[i][j].char, self.blocktype.blocks[i][j].colorpair)
        
    def type(self):
        return self.blocktypestr

        # self.screen.addstr(self.locX, self.locY, str(self.blocktype.blocks), curses.color_pair(9))
    
    def coords(self):
        return self.y, self.x

