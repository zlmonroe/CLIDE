if __name__ == "__main__":
    import __fixDir__

import tkinter


class MenuBar(tkinter.Frame):
    def __init__(self, root, activebackground="#4B6EAF", textColor="white", *args, **kwargs):
        tkinter.Frame.__init__(self, root, *args, **kwargs)

        fileButton = tkinter.Menubutton(self, text="File", bg=self["background"], activebackground=activebackground, foreground=textColor)
        fileButton.pack(side=tkinter.LEFT)
        fileMenu = tkinter.Menu(self, tearoff=0)
        fileMenu.add_command(label="New")
        fileButton["menu"] = fileMenu

        editMenu = tkinter.Menu(self, tearoff=0)
        # fileMenu.pack()
        #self.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Cut")
        editMenu.add_command(label="Copy")
        editMenu.add_command(label="Paste")

        try:
            self.master.config(menu=self)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(root, "config", "-menu", self)