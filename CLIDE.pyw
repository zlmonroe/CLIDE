import tkinter
from _tkinter import TclError

from CLIDElib.PyConsole import PyConsole
from CLIDElib.CodeBox import CodeBox
from CLIDElib.LineNumbers import LineNumbers
from CLIDElib.MenuBar import MenuBar
from CLIDElib.DirectoryBrowser import DirectoryBrowser

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

        # create a toplevel menu
        menubar = MenuBar(self, activebackground="#4B6EAF", background="#3C3F41", textColor="#BBBBBB")
        menubar.pack(side=tkinter.TOP, anchor="n", expand=False, fill="x")

        # display the menu
        self.config(menu=menubar)

        self.mainPaneWindow = tkinter.PanedWindow(self, orient="vertical")
        self.mainPaneWindow.pack(fill="both", expand=True)

        textFrame = tkinter.Frame(self)

        self.text = CodeBox(textFrame)
        self.lineNumbers = LineNumbers(textFrame, self.text)

        self.lineNumbers.pack(side=tkinter.LEFT, expand=False, fill="y")
        self.text.pack(side=tkinter.RIGHT, expand=True, fill="both")

        self.smallerPaneWindow = tkinter.PanedWindow(self.mainPaneWindow, orient="horizontal")
        explorer = DirectoryBrowser(self.smallerPaneWindow, background="#3C3F41")
        self.smallerPaneWindow.add(explorer)
        self.smallerPaneWindow.add(textFrame)
        self.smallerPaneWindow.pack(expand=True, fill="both")

        self.mainPaneWindow.add(self.smallerPaneWindow)

        self.terminal = PyConsole(self, height=10)

        def closeAndKill():
            self.terminal.close()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", closeAndKill)
        self.terminal.bind("<<Process Ended>>", lambda e: self.text.focus_set())

        self.mainPaneWindow.add(self.terminal)

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
