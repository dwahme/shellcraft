import curses
from enum import Enum
from queue import Queue, Empty
from subprocess import Popen, run, PIPE
from threading import Thread

class Port(Enum):
    RIGHT = 0
    BOTTOM = 1
    LEFT = 2
    TOP = 3


class Computer:
    CWD = "./computer_files"
    
    def __init__(self, name, block):
        self.name = name
        self.run_command = "python3"
        self.block = block

        self.process = None
        self.read_thread = None

        self.out_ports = [Queue() for _ in range(4)]

        self.port_table = {}

    # Queues output from a process to be read later
    def enqueue_output(self, out, queues):
        for line in iter(out.readline, b''):
            output = line.decode("utf-8").split(" ", 1)

            # Expects [<port>, <msg>]
            queue = queues[int(output[0])]
            queue.put(output[1])

        out.close()

    # Opens up a text editor for a given computer
    def editor(self, stdscr, editor="vim"):
        curses.endwin()
        run([editor, "{}".format(self.name)], cwd=Computer.CWD)
        stdscr.refresh()
        curses.curs_set(0)

    # Runs a computer's file and starts queueing its output into self.out_queue
    def run(self):
        # Start the process to run the computer's program
        self.process = Popen([self.run_command, "{}".format(self.name)], 
                             cwd=Computer.CWD,  stdout=PIPE, stdin=PIPE)

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
        data = read_port(out_port)

        for c in self.port_table[out_port]:
            c.send_port

    # Queues data to be sent in
    def send_port(self, port, msg):
        to_send = bytes("{} {}".format(port, msg))

        self.process.communicate(input=to_send)

    # Performs BFS across wires given a starting point and adds computers to queue
    def __update_network(self, world, start):
        queue = Queue()
        queue.put(start)

        checked = { block.coords(), start }

        found_ports = []
        
        while not queue.empty():

            y, x, port = queue.get()
            block = world[y][x]

            if "WIRE" in block.blocktypestr:
                dirs = block.blocktypestr.split("_")

                if "T" in dirs and (y, x) not in checked:
                    queue.add((y - 1, x, Port.BOTTOM))
                    checked.add((y - 1, x))

                if "B" in dirs and (y, x) not in checked:
                    queue.add((y + 1, x, Port.TOP))
                    checked.add((y + 1, x))

                if "R" in dirs and (y, x) not in checked:
                    queue.add((y, x + 1, Port.LEFT))
                    checked.add((y, x + 1))

                if "L" in dirs and (y, x) not in checked:
                    queue.add((y, x - 1, Port.RIGHT))
                    checked.add((y, x - 1))

            elif block.blocktypestr == "COMP":
                found_ports.append((y, x, port))

        return found_ports

    # Finds the networks across each port
    def update_network(self, world):
        y, x = self.block.coords()

        port_table[Port.RIGHT] = __update_network(world, (y, x + 1, Port.LEFT))
        port_table[Port.BOTTOM] = __update_network(world, (y + 1, x, Port.TOP))
        port_table[Port.LEFT] = __update_network(world, (y, x - 1, Port.RIGHT))
        port_table[Port.TOP] = __update_network(world, (y - 1, x, Port.BOTTOM))