import curses
from queue import Queue, Empty
from subprocess import Popen, run, PIPE
from threading import Thread


class Computer:
    
    def __init__(self, name):
        self.name = name
        self.run_command = ""
        self.process = None
        self.read_thread = None
        self.out_queue = None

    def enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    def editor(self, stdscr):
        curses.endwin()
        run(["vim", "{}".format(self.name)], cwd="./computer_files")
        stdscr.refresh()

        self.process = Popen(["python3", "{}".format(self.name)], cwd="./computer_files",  stdout=PIPE)
        self.out_queue = Queue()
        self.read_thread = Thread(target=self.enqueue_output, args=(self.process.stdout, self.out_queue))
        self.read_thread.daemon = True # thread dies with the program
        self.read_thread.start()

        curses.curs_set(0)

    def read_pipe(self):

        done = False
        out = ""

        while not done:
            try:
                line = self.out_queue.get_nowait()
            except Empty:
                done = True
            else:
                out += line.decode("utf-8")
        
        return out
