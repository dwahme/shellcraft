from curses.textpad import rectangle
from operator import attrgetter
from queue import Queue, Empty
from .utils.chilog import chilog

class Monitor:

    def __init__(self, blocks):
        self.blocks = blocks
        self.id = 0
        self.text = ["hi"]


    def bounds(self):
        coords = [b.coords() for b in self.blocks]
        min_y = min([y for (y, _) in coords])
        max_y = max([y for (y, _) in coords])
        min_x = min([x for (_, x) in coords])
        max_x = max([x for (_, x) in coords])

        return min_y, max_y, min_x, max_x

    def generate_iomonitors(self):
        ios = []

        for b in self.blocks:
            IOMonitor(b, self)

        return ios


    def in_bounds(self, y, x):
        return (y, x) in [b.coords() for b in self.blocks]

    def num_blocks(self):
        min_y, max_y, min_x, max_x = self.bounds()
        return (max_y - min_y + 1) * (max_x - min_x + 1)

    def is_rectangle(self):
        return self.num_blocks() == len(self.blocks)

    def box_bounds(self):
        min_y, max_y, min_x, max_x = self.bounds()
        top, bot = 0, (max_y - min_y + 1) * 3 - 1
        left, right = 0, (max_x - min_x + 1) * 5 - 1

        return top, left, bot, right

    def write(self, txt):
        top, left, bot, right = self.box_bounds()
        
        lines = txt.split("\n")

        for line in lines:
            sublines = [line[i:i + (right - 2)] for i in range(0, len(line), (right - 2))]
            for sub in sublines:
                self.text.append(sub)
            
        self.text = self.text[-(bot - 2):-1]

    def render(self, stdscr, y, x):
        if self.is_rectangle():

            top, left, bot, right = self.box_bounds()


            # for j in range(1, bot - 1):
            #     for i in range(1, right - 1):
            #         stdscr.addstr(y + j, x + i, str(self.id) * 4)
            for j in range(1, bot):
                s = " " * (right - 1)

                if len(self.text) >= j:
                    t = self.text[j - 1]
                    s = t + s[len(t):]
                
                stdscr.addstr(y + j, x + 1, s)

            rectangle(stdscr, top + y, left + x, bot + y, right + x)

            return True
        
        return False

    def find_monitor(blocks, y, x):
        for block in blocks:
            if (y, x) == block.coords():
                return block
        
        return None

    def __aggregate_monitors(m_blocks):
        coords = [m.coords() for m in m_blocks]

        start = m_blocks[0]

        y, x = start.coords()

        queue = Queue()
        queue.put((y, x))

        visited = set()
        visited.add((y, x))

        found_monitors = [(y, x)]

        while not queue.empty():

            y, x = queue.get()

            if (y - 1, x) not in visited and (y - 1, x) in coords:
                queue.put((y - 1, x))
                found_monitors.append((y - 1, x))
                visited.add((y - 1, x))

            if (y + 1, x) not in visited and (y + 1, x) in coords:
                queue.put((y + 1, x))
                found_monitors.append((y + 1, x))
                visited.add((y + 1, x))

            if (y, x + 1) not in visited and (y, x + 1) in coords:
                queue.put((y, x + 1))
                found_monitors.append((y, x + 1))
                visited.add((y, x + 1))

            if (y, x - 1) not in visited and (y, x - 1) in coords:
                queue.put((y, x - 1))
                found_monitors.append((y, x - 1))
                visited.add((y, x - 1))
                
        out = [Monitor.find_monitor(m_blocks, y, x) for (y, x) in found_monitors]
        return [b for b in out if b]

    def aggregate_monitors(monitor_list):

        # Flatten all the game's monitors
        monitors = [monitor.blocks for monitor in monitor_list]
        monitor_blocks = [block for m in monitors for block in m]

        new_monitors = []

        tmp = 1

        while monitor_blocks != []:
            ms = Monitor.__aggregate_monitors(monitor_blocks)
            monitor_blocks = [b for b in monitor_blocks if b not in ms]

            # Sort the monitors and make a new Monitor object
            ms.sort(key=attrgetter("coord_prop"))
            new_monitors.append(Monitor(ms))
            new_monitors[-1].id = tmp
            tmp += 1

        return new_monitors


class IOMonitor:

    def __init__(self, block, parent):
        self.block = block
        self.parent = parent

    def send_port(self, port, data):
        return monitor.write(data)
