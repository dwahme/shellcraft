import curses
from curses.textpad import Textbox, rectangle
from .utils.chilog import chilog
from enum import IntEnum
from queue import Queue, Empty
from subprocess import Popen, run, PIPE
from threading import Thread

class Port(IntEnum):
    RIGHT = 0
    BOTTOM = 1
    LEFT = 2
    TOP = 3


class Computer:
    CWD = "./computer_files"
    EDITOR = "vim"
    
    def __init__(self, block):
        self.name = None
        self.runtime = None
        self.block = block

        self.process = None
        self.read_thread = None

        self.out_ports = [Queue() for _ in range(4)]

        self.port_table = {}

    def new_computer_prompt(self, stdscr):
        # Leave the textbox on enter
        exit_func = lambda k: 7 if k == 10 else k

        h, w = 5, 30
        term_h, term_w = stdscr.getmaxyx()
        y, x = (term_h - h) // 2, (term_w - w) // 2

        editwin = curses.newwin(h + 2, w + 2, y, x)
        rectangle(stdscr, y - 1, x - 1, y + h + 2, x + w + 2)
        stdscr.addstr(y - 1, x + 1, "Enter a computer name")
        stdscr.refresh()

        box = Textbox(editwin)

        # Let the user edit until Ctrl-G is struck.
        box.edit(exit_func)

        # Get resulting contents
        self.name = box.gather().strip()

        editwin = curses.newwin(h + 2, w + 2, y, x)
        rectangle(stdscr, y - 1, x - 1, y + h + 2, x + w + 2)
        stdscr.addstr(y - 1, x + 1, "Enter a runtime command")
        stdscr.refresh()

        box = Textbox(editwin)

        box.edit(exit_func)

        # Get resulting contents
        self.runtime = box.gather().strip().split()


    # Queues output from a process to be read later
    def enqueue_output(self, out, queues):
        for line in iter(out.readline, b''):
            output = line.decode("utf-8").split(" ", 1)

            # Expects [<port>, <msg>]
            queue = queues[int(output[0])]
            queue.put(output[1])

        out.close()

    # Opens up a text editor for a given computer
    def editor(self, stdscr):
        curses.endwin()
        run([Computer.EDITOR, "{}".format(self.name)], cwd=Computer.CWD)
        stdscr.refresh()
        curses.curs_set(0)

    # Runs a computer's file and starts queueing its output into self.out_queue
    def run(self):
        # Start the process to run the computer's program
        self.process = Popen(self.runtime, cwd=Computer.CWD, 
                             stdout=PIPE, stdin=PIPE)

        # Begin queueing the output
        self.read_thread = Thread(target=self.enqueue_output, 
                                  args=(self.process.stdout, self.out_ports))
        self.read_thread.daemon = True # thread dies with the program
        self.read_thread.start()

    # Gets all queued output from a computer's process (or None if no output)
    def read_port(self, port):

        empty = False
        out = None
        out_port = self.out_ports[port]

        while not empty:
            try:
                line = out_port.get_nowait()
            except Empty:
                empty = True
            else:
                if out == None:
                    out = ""

                out += line

        return out

    def broadcast(self, out_port):
        data = self.read_port(out_port)

        for (c, p) in self.port_table[out_port]:
            c.send_port(p, data)

    def broadcast_all(self):
        for port in self.port_table.keys():
            self.broadcast(port)

    # Queues data to be sent in
    def send_port(self, port, msg):
        to_send = bytes("{} {}".format(port, msg), 'utf-8')

        if self.process != None:
            self.process.communicate(input=to_send)

    def find_computer(computers, y, x):
        for computer in computers:
            if computer.block.coords() == (y, x):
                return computer
        
        return None

    # Performs BFS across wires given a starting point and adds computers to queue
    def __update_network(self, world, computers, start):
        y, x, _ = start
        x %= world.max_x
        
        blocktype = world.map[y][x].blocktypestr
        if "WIRE" not in blocktype and blocktype != "COMP":
            return []

        queue = Queue()
        queue.put(start)

        checked = { self.block.coords() }

        found_ports = []
        
        while not queue.empty():

            y, x, port = queue.get()
            x %= world.max_x

            chilog("{} {}\n".format(y, x))

            block = world.map[y][x]

            if "WIRE" in block.blocktypestr:
                dirs = block.blocktypestr.split("_")[1]

                chilog("    WIRE: {} {}\n".format((y, x), dirs))

                if "T" in dirs and (y - 1, x) not in checked:
                    queue.put((y - 1, x, Port.BOTTOM))
                    checked.add((y - 1, x))

                if "B" in dirs and (y + 1, x) not in checked:
                    queue.put((y + 1, x, Port.TOP))
                    checked.add((y + 1, x))

                if "R" in dirs and (y, x + 1) not in checked:
                    queue.put((y, x + 1, Port.LEFT))
                    checked.add((y, x + 1))

                if "L" in dirs and (y, x - 1) not in checked:
                    queue.put((y, x - 1, Port.RIGHT))
                    checked.add((y, x - 1))

            elif block.blocktypestr == "COMP":
                found_ports.append((y, x, port))

        chilog("BFS: {} {}\n".format(start, found_ports))

        return [(Computer.find_computer(computers, y, x), p) for (y, x, p) in found_ports]

    # Finds the networks across each port
    def update_network(self, world, computers):
        y, x = self.block.coords()

        self.port_table[Port.RIGHT] = self.__update_network(world, computers, (y, x + 1, Port.LEFT))
        self.port_table[Port.BOTTOM] = self.__update_network(world, computers, (y + 1, x, Port.TOP))
        self.port_table[Port.LEFT] = self.__update_network(world, computers, (y, x - 1, Port.RIGHT))
        self.port_table[Port.TOP] = self.__update_network(world, computers, (y - 1, x, Port.BOTTOM))

        
