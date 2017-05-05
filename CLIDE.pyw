import tkinter
from tkinter import ttk
from _tkinter import TclError

from CLIDElib.PyConsole import PyConsole
from CLIDElib.CodeBox import CodeBox
from CLIDElib.LineNumbers import LineNumbers

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class IDE(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Untitled")
        try:
            self.iconbitmap("CLIDE.ico")
        except TclError:
            pass
        
        self.sliders = ttk.PanedWindow(orient="vertical")
        self.sliders.pack(fill="both", expand=True)

        textFrame = tkinter.Frame(self)

        self.text = CodeBox(textFrame)
        self.text.pack(side=tkinter.RIGHT)

        self.lineNumbers = LineNumbers(textFrame, self.text)
        self.lineNumbers.pack(side=tkinter.LEFT)

        self.sliders.add(textFrame)

        self.terminal = PyConsole(self, height=10)
        self.terminal.bind("<<Process Ended>>", lambda e: self.text.focus_set())

        self.sliders.add(self.terminal)

        self.bind("<F5>", self.runLisp)

    def runLisp(self, event):
        self.terminal.replace("1.0", tkinter.END, "")

        with open("test.lsp", "w+") as file:
            file.write(self.text.get("1.0", tkinter.END) + "\r\n")

        cmd = [dir_path + "/ccl/wx86cl64.exe", "-l", "test.lsp"]
        # cmd = ["cmd.exe"]
        self.terminal.startNew(cmd)


def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return


if __name__ == "__main__":
    root = IDE()
    root.mainloop()
