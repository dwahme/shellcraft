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
        self.out_queue = Queue()

    # Queues output from a process to be read later
    def enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
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
                             cwd=Computer.CWD,  stdout=PIPE)

        # Begin queueing the output
        self.read_thread = Thread(target=self.enqueue_output, 
                                  args=(self.process.stdout, self.out_queue))
        self.read_thread.daemon = True # thread dies with the program
        self.read_thread.start()

    # Gets all queued output from a computer's process (or None if no output)
    def read_pipe(self):

        empty = False
        out = None

        while not empty:
            try:
                line = self.out_queue.get_nowait()
            except Empty:
                empty = True
            else:
                if out == None:
                    out = ""

                out += line.decode("utf-8")

        return out
