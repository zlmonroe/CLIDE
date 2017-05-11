if __name__ == "__main__":
    import __fixDir__

import tkinter


class MenuBar(tkinter.Frame):
    def __init__(self, clide, activebackground="#4B6EAF", textColor="white", *args, **kwargs):
        tkinter.Frame.__init__(self, clide, *args, **kwargs)

        fileButton = tkinter.Menubutton(self, text="File", bg=self["background"],
                                        activebackground=activebackground, foreground=textColor,
                                        underline=0)
        fileButton.pack(side=tkinter.LEFT)
        fileMenu = tkinter.Menu(fileButton, tearoff=0)
        fileMenu.add_command(label="New", command=clide.new)
        fileMenu.add_command(label="Save", command=clide.save)
        fileMenu.add_command(label="Open", command=clide.open)
        fileButton["menu"] = fileMenu

        editButton = tkinter.Menubutton(self, text="Edit", bg=self["background"],
                                        activebackground=activebackground, foreground=textColor)
        editButton.pack(side=tkinter.LEFT)
        editMenu = tkinter.Menu(editButton, tearoff=0)
        editMenu.add_command(label="Find", command=clide.find)
        editButton["menu"] = editMenu

        self._stopImage = tkinter.PhotoImage(file="stop.png")
        stopButton = tkinter.Button(self, image=self._stopImage, borderwidth=0, bg=self["background"],
                                    command=clide.terminal.close)
        stopButton.pack(side=tkinter.RIGHT, padx=10)

        self._runImage = tkinter.PhotoImage(file="run.png")
        runButton = tkinter.Button(self, image=self._runImage, borderwidth=0, bg=self["background"], command=clide.runLisp)
        runButton.pack(side=tkinter.RIGHT, padx=10)

        try:
            self.master.config(menu=self)
        except AttributeError:
            self.master.tk.call(clide, "config", "-menu", self)