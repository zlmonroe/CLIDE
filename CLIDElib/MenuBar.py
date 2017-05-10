if __name__ == "__main__":
    import __fixDir__

import tkinter


class MenuBar(tkinter.Frame):
    def __init__(self, root, activebackground="#4B6EAF", textColor="white", *args, **kwargs):
        tkinter.Frame.__init__(self, root, *args, **kwargs)

        fileButton = tkinter.Menubutton(self, text="File", bg=self["background"],
                                        activebackground=activebackground, foreground=textColor,
                                        underline=0)
        fileButton.pack(side=tkinter.LEFT)
        fileMenu = tkinter.Menu(fileButton, tearoff=0)
        fileMenu.bind("<Leave>", lambda e: print("ran"))
        fileMenu.add_command(label="New", command=lambda: print("new"))
        fileMenu.add_command(label="Save", command=lambda: print("save"))
        fileButton["menu"] = fileMenu

        editButton = tkinter.Menubutton(self, text="Edit", bg=self["background"],
                                        activebackground=activebackground, foreground=textColor)
        editButton.pack(side=tkinter.LEFT)
        editMenu = tkinter.Menu(editButton, tearoff=0)
        editMenu.add_command(label="Find", command=lambda: print("find"))
        editButton["menu"] = editMenu


        try:
            self.master.config(menu=self)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(root, "config", "-menu", self)