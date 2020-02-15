import curses
from queue import Queue, Empty
from subprocess import Popen, run, PIPE
from threading import Thread


class Computer:
    CWD = "./computer_files"
    
    def __init__(self, name):
        self.name = name
        self.run_command = "python3"

        self.process = None
        self.read_thread = None

        self.out_ports = [Queue() for _ in range(4)]

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

                out += line.decode("utf-8")

        return out

    # Queues data to be sent in
    def send_port(self, port, msg):
        to_send = bytes("{} {}".format(port, msg))

        self.process.communicate(input=to_send)
