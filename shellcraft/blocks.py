import curses
import sys
from enum import Enum 
from . pixel import Pixel

class MType():
    """
    Special Monitor type blocks where text-morphism is crucial
    """
    def __init__(self, blocktype):
        blocklist = {
            "MONITORBASIC": [
                [
                    Pixel(" ", 15, 0, 301), 
                    Pixel(" ", 15, 0, 302),
                    Pixel(" ", 15, 0, 303),
                    Pixel(" ", 15, 0, 304),
                    Pixel(" ", 15, 0, 305),

                ], 
                [
                    Pixel(" ", 15, 0, 306),
                    Pixel(" ", 15, 0, 307),
                    Pixel(" ", 15, 0, 308),
                    Pixel(" ", 15, 0, 309),
                    Pixel(" ", 15, 0, 310),

                ],
                [
                    Pixel(" ", 15, 0, 311),
                    Pixel(" ", 15, 0, 312),
                    Pixel(" ", 15, 0, 313),
                    Pixel(" ", 15, 0, 314),
                    Pixel(" ", 15, 0, 315),
                ]
            ]
        }
        self.blocks = blocklist[blocktype]
    

class ZType():
    """
    Special Monster type blocks where text-morphism is crucial
    """
    def __init__(self, blocktype):
        blocklist = {
            "MONSTERSLIME": [
                [
                    Pixel(" ", 15, 40, 241), 
                    Pixel(" ", 15, 34, 242),
                    Pixel(" ", 226, 34, 243),
                    Pixel(" ", 15, 40, 244),
                    Pixel(" ", 15, 40, 245),

                ], 
                [
                    Pixel(" ", 15, 40, 246),
                    Pixel("o", 0, 40, 247),
                    Pixel("w", 0, 40, 248),
                    Pixel("o", 0, 40, 249),
                    Pixel(" ", 15, 40, 250),

                ],
                [
                    Pixel(" ", 15, 28, 251),
                    Pixel(" ", 15, 28, 252),
                    Pixel(" ", 15, 40, 253),
                    Pixel(" ", 15, 40, 254),
                    Pixel(" ", 15, 34, 255),
                ]
            ]
        }
        self.blocks = blocklist[blocktype]
    

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
                    Pixel(" ", 16, 0, 124), 
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),

                ], 
                [
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),

                ],
                [
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                    Pixel(" ", 16, 0, 124),
                ]
            ],
            "WEEDS": [
                [
                    Pixel("§", 28, 34, 106), 
                    Pixel(" ", 16, 0, 107),
                    Pixel(" ", 16, 0, 108),
                    Pixel(" ", 16, 0, 109),
                    Pixel(" ", 28, 0, 110),

                ], 
                [
                    Pixel("§", 28, 28, 111),
                    Pixel(" ", 16, 0, 112),
                    Pixel("§", 28, 28, 113),
                    Pixel(" ", 16, 0, 114),
                    Pixel("§", 28, 28, 115),

                ],
                [
                    Pixel("\\", 28, 22, 116),
                    Pixel(" ", 28, 22, 117),
                    Pixel(" ", 28, 22, 118),
                    Pixel(" ", 28, 22, 119),
                    Pixel("/", 28, 22, 120),
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
            "BEDROCK": [
                [
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),

                ], 
                [
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                   
                ],
                [
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    Pixel(" ", 16, 245, 7),
                    
                ]
            ],
            "TNT": [ #125-130 available
                [
                    Pixel(" ", 16, 124, 125),
                    Pixel(" ", 16, 160, 126),
                    Pixel(" ", 16, 124, 125),
                    Pixel(" ", 16, 160, 126),
                    Pixel(" ", 16, 124, 125),

                ], 
                [
                    Pixel(" ", 16, 254, 127),
                    Pixel("T", 0, 255, 128),
                    Pixel("N", 0, 254, 127),
                    Pixel("T", 0, 255, 128),
                    Pixel(" ", 16, 254, 127),
                   
                ],
                [
                    Pixel(" ", 16, 124, 125),
                    Pixel(" ", 16, 160, 126),
                    Pixel(" ", 16, 124, 125),
                    Pixel(" ", 16, 160, 126),
                    Pixel(" ", 16, 124, 125),
                    
                ]
            ],
            "OBSIDIAN": [
                [
                    Pixel(" ", 16, 55, 123), 
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),

                ], 
                [
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),

                ],
                [
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
                    Pixel(" ", 16, 55, 123),
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
            "PLAYERNORMAL": [
                [
                    Pixel("^", 16, 212, 136), 
                    Pixel(" ", 16, 0, 137),
                    Pixel(" ", 16, 0 , 138),
                    Pixel(" ", 16, 0, 139),
                    Pixel("^", 16, 212, 140),

                ], 
                [
                    Pixel("u", 16, 212, 141),
                    Pixel(" ", 16, 212, 142),
                    Pixel("w", 16, 212, 143),
                    Pixel(" ", 16, 212, 144),
                    Pixel("u", 16, 212, 145),

                ],
                [
                    Pixel(" ", 16, 212, 146),
                    Pixel(" ", 16, 212, 147),
                    Pixel(" ", 16, 212, 148),
                    Pixel(" ", 16, 212, 149),
                    Pixel(" ", 16, 212, 150),
                ]
            ],
            "PLAYERPLACE": [
                [
                    Pixel("^", 16, 212, 166), 
                    Pixel(" ", 16, 0, 167),
                    Pixel("P", 16, 34, 168),
                    Pixel(" ", 16, 0, 169),
                    Pixel("^", 16, 212, 170),

                ], 
                [ 
                    Pixel("u", 16, 212, 171),
                    Pixel(" ", 16, 212, 172),
                    Pixel("w", 16, 212, 173),
                    Pixel(" ", 16, 212, 174),
                    Pixel("u", 16, 212, 175),

                ],
                [
                    Pixel(" ", 16, 212, 176),
                    Pixel(" ", 16, 212, 177),
                    Pixel(" ", 16, 212, 178),
                    Pixel(" ", 16, 212, 179),
                    Pixel(" ", 16, 212, 180),
                ]
            ],
            "PLAYERINTERACT": [
                [
                    Pixel("^", 16, 212, 181), 
                    Pixel(" ", 16, 0, 182),
                    Pixel("I", 15, 21, 183),
                    Pixel(" ", 16, 0, 184),
                    Pixel("^", 16, 212, 185),

                ], 
                [
                    Pixel("u", 16, 212, 186),
                    Pixel(" ", 16, 212, 187),
                    Pixel("w", 16, 212, 188),
                    Pixel(" ", 16, 212, 189),
                    Pixel("u", 16, 212, 190),

                ],
                [
                    Pixel(" ", 16, 212, 191),
                    Pixel(" ", 16, 212, 192),
                    Pixel(" ", 16, 212, 193),
                    Pixel(" ", 16, 212, 194),
                    Pixel(" ", 16, 212, 195),
                ]
            ],
            "PLAYERBREAK": [
                [
                    Pixel("^", 16, 212, 196), 
                    Pixel(" ", 16, 0, 197),
                    Pixel("B", 15, 197, 198),
                    Pixel(" ", 16, 0, 199),
                    Pixel("^", 16, 212, 200),

                ], 
                [
                    Pixel("u", 16, 212, 201),
                    Pixel(" ", 16, 212, 202),
                    Pixel("w", 16, 212, 203),
                    Pixel(" ", 16, 212, 204),
                    Pixel("u", 16, 212, 205),

                ],
                [
                    Pixel(" ", 16, 212, 206),
                    Pixel(" ", 16, 212, 207),
                    Pixel(" ", 16, 212, 208),
                    Pixel(" ", 16, 212, 209),
                    Pixel(" ", 16, 212, 210),
                ]
            ],
            "PI": [
                [
                    Pixel("-", 16, 253, 211), 
                    Pixel("-", 16, 253, 212),
                    Pixel("-", 16, 253, 213),
                    Pixel("-", 16, 253, 214),
                    Pixel("-", 16, 253, 215),

                ], 
                [
                    Pixel("¦", 16, 253, 216),
                    Pixel("'", 16, 40, 217),
                    Pixel("v", 16, 40, 218),
                    Pixel("'", 16, 40, 219),
                    Pixel("¦", 16, 253, 220),

                ],
                [
                    Pixel("-", 16, 253, 221),
                    Pixel("-", 16, 253, 222),
                    Pixel("-", 16, 253, 223),
                    Pixel("-", 16, 253, 224),
                    Pixel("-", 16, 253, 225),
                ]
            ],



            "DIAMOND": [
                [
                    Pixel(" ", 16, 15, 226), 
                    Pixel(" ", 16, 241, 227),
                    Pixel(" ", 16, 44, 228),
                    Pixel(" ", 16, 43, 229),
                    Pixel(" ", 16, 14, 230),

                ], 
                [
                    Pixel(" ", 16, 87, 231),
                    Pixel(" ", 16, 242, 232),
                    Pixel(" ", 16, 239, 233),
                    Pixel(" ", 16, 81, 234),
                    Pixel(" ", 16, 194, 235),

                ],
                [
                    Pixel(" ", 16, 50, 236),
                    Pixel(" ", 16, 195, 237),
                    Pixel(" ", 16, 195, 238),
                    Pixel(" ", 16, 243, 239),
                    Pixel(" ", 16, 243, 240),
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
        if ("MONITOR" in blocktype):
            self.blocktype = MType(blocktype)
        elif ("MONSTER" in blocktype):
            self.blocktype = ZType(blocktype)
        else:
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
    
    @property
    def coord_prop(self):
        return self.y, self.x

    def coords(self):
        return self.y, self.x

    def morph(self, blocktype): 
        """
        Changes a given block's representation without altering memory
        """
        self.blocktypestr = blocktype
        self.blocktype = Btype(blocktype)
