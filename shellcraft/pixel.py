import curses

class Pixel:
    def __init__(self, char, txtcolor, bgcolor, pairindex):
        curses.init_pair(pairindex, txtcolor, bgcolor)
        self.char = char
        self.txtcolor = txtcolor
        self.bgcolor = bgcolor
        self.colorpair = curses.color_pair(pairindex)

    