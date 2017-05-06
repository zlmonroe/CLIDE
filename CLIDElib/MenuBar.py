if __name__ == "__main__":
    import __fixDir__

import tkinter


class MenuBar(tkinter.Menu):
    def __init__(self, root, *args, **kwargs):
        tkinter.Menu.__init__(self, *args, **kwargs)

        fileMenu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New")

        editMenu = tkinter.Menu(self, tearoff=0)
        self.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Cut")
        editMenu.add_command(label="Copy")
        editMenu.add_command(label="Paste")

        try:
            self.master.config(menu=self)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(root, "config", "-menu", self)