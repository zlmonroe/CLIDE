import tkinter
from _tkinter import TclError
from tkinter import filedialog, messagebox

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

        self.mainPaneWindow = tkinter.PanedWindow(self, orient="vertical")
        self.mainPaneWindow.pack(fill="both", expand=True, side=tkinter.BOTTOM)

        textFrame = tkinter.Frame(self)

        self.text = CodeBox(textFrame, wrap="none", undo=True)
        self.lastSave = ""
        self.lineNumbers = LineNumbers(textFrame, self.text)

        self.lineNumbers.pack(side=tkinter.LEFT, expand=False, fill="y")
        self.text.pack(side=tkinter.RIGHT, expand=True, fill="both")

        self.smallerPaneWindow = tkinter.PanedWindow(self.mainPaneWindow, orient="horizontal")
        explorer = DirectoryBrowser(self.smallerPaneWindow, background="#3C3F41", )
        self.smallerPaneWindow.add(explorer)
        self.smallerPaneWindow.add(textFrame)
        self.smallerPaneWindow.pack(expand=True, fill="both")

        self.mainPaneWindow.add(self.smallerPaneWindow)

        explorer.bind("<<Retrieved File>>", lambda e: self.open(file=explorer.file))

        self.terminal = PyConsole(self, height=10)

        def closeAndKill():
            self.terminal.close()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", closeAndKill)
        self.terminal.bind("<<Process Ended>>", lambda e: self.text.focus_set())

        self.mainPaneWindow.add(self.terminal)

        self.bind("<F5>", self.runLisp)

        # create a toplevel menu
        menubar = MenuBar(self, activebackground="#4B6EAF", background="#3C3F41", textColor="#BBBBBB")
        menubar.pack(side=tkinter.TOP, anchor="n", expand=False, fill="x")

    def runLisp(self, event=None):
        self.terminal.replace("1.0", tkinter.END, "")

        with open("test.lsp", "w+") as file:
            file.write(self.text.get("1.0", tkinter.END) + "\r\n")

        cmd = [dir_path + "/ccl/wx86cl64.exe", "-l", "test.lsp"]
        # cmd = ["cmd.exe"]
        self.terminal.startNew(cmd)

    def save(self, event=None):
        with filedialog.asksaveasfile(mode='w+', defaultextension=".lsp") as f:
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            contents = str(self.text.get("1.0", "end"))
            f.write(contents)
            self.lastSave = contents

    def new(self, event=None):
        if self.text.get("1.0", "end") != "":
            if self.lastSave == self.text.get("1.0", "end") or \
                    messagebox.askyesno("Confirm", "Really close? (this will delete any unsaved progress!)"):
                self.text.replace("1.0", "end", "")

    def open(self, event=None, filePath=None, file=None):
        if filePath is None and file is None:
            file = filedialog.askopenfile(mode="r")
        elif filePath is None:
            file = open(file, "r")
        if file is not None: # user can still cancel during filedialog choice
            if self.text.get("1.0", "end") == "\n" or self.lastSave == self.text.get("1.0", "end") or \
                    messagebox.askyesno("Confirm", "Really close? (this will delete any unsaved progress!)"):
                self.text.replace("1.0", "end", file.read())
                self.lastSave = self.text.get("1.0", "end")
            file.close()

    def find(self, event=None):
        messagebox.showinfo("Sorry!", "Find has not yet been implemented. \n:-(")

if __name__ == "__main__":
    root = IDE()
    root.mainloop()
