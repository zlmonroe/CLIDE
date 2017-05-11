if __name__ == "__main__":
    import __fixDir__

from queue import Queue, Empty
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
from time import sleep

from CLIDElib.StdIO import StdIO

DEBUG = False


def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return


class PyConsole(StdIO):
    def __init__(self, root, command=(), bg="black", fg="white", *args, **kwargs):
        StdIO.__init__(self, root, bg=bg, fg=fg, insertbackground=fg, *args, **kwargs)

        self.process = None
        self.readThread = None
        self.inQ = None
        self.writeThread = None

        if command:
            self.startNew(command)

        self.bind("<a>", lambda e: self.close)

    def startNew(self, command):
        if DEBUG: print("Starting new process")
        if self.process:
            self.write("Atempting to kill process\n")
            self.process.kill()
            self.event_generate("<<Process Ended>>")

        self.process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        if not self.readThread or not self.readThread.is_alive():
            self.readThread = Thread(target=self.sendIn, args=[])
            self.readThread.daemon = True
            self.readThread.start()

        if not self.writeThread or not self.writeThread.is_alive():
            self.inQ = Queue()
            self.insertNewLine()

            self.writeThread = Thread(target=self.readOut, args=[])
            self.writeThread.daemon = True
            self.writeThread.start()

        self.focus_set()
        self.mark_set("insert", "end")
        self.see("end")

    def sendIn(self):
        while self.process:
            if self.process:
                line = self.readline(timeout=1000)
                if DEBUG and line == "": print("Read timeout")
                line += "\n"
                if line == "clear\n" or line == "cls\n":
                    self.replace("1.0", "end", "")
                elif line == "exit\n":
                    self.event_generate("<<Process Ended>>")
                    self.write("Process forcibly closed...\n")
                elif line != "\n":
                    try:
                        self.process.stdin.write(line.encode("UTF-8"))
                        self.process.stdin.flush()
                    except OSError:
                        self.write("Write to process failed, process has ended unexpectedly...\n")
                        self.process.kill()
                        self.process = None
                        self.event_generate("<<Process Ended>>")
                    except AttributeError:
                        pass
        if DEBUG: print("Finished reading all input, thread will now exit and signal end of process")
        self.close()

    def readOut(self):
        """ needs to be in a thread so we can read the stdout w/o blocking """
        while self.process and self.process.stdout is not None:
            output = self.process.stdout.read(1)
            if output == b'':
                if self.process:
                    self.process.stdout = None
                    self.process = None
            if output:
                self.inQ.put(output)
        sleep(1)
        if DEBUG: print("Finished all output, thread will now exit")

    def insertNewLine(self):
        """update GUI with items from the inQueue."""
        for line in iter_except(self.inQ.get_nowait, Empty):  # display all content
            if not line is None:
                self.write(line)

        self.after(30, self.insertNewLine)  # schedule next update

    def close(self):
        if self.process is not None:
            process, self.process = self.process, None
            process.kill()
        else:
            self.write("Process terminated!\n")

        self.event_generate("<<Process Ended>>")


if __name__ == "__main__":
    import tkinter

    root = tkinter.Tk()
    console = PyConsole(root)
    console.startNew(["cmd.exe"])


    def startNewOne(event):
        console.write("You ended cmd.......\nI'm going to start another one now.")
        console.startNew(["cmd.exe"])


    console.bind("<<Process Ended>>", startNewOne)
    console.pack()
    root.mainloop()
