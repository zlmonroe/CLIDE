"""A directory browser using Ttk self.treeview.

Based on the demo found in Tk 8.5 library/demos/browse and from
https://svn.python.org/projects/python/trunk/Demo/tkinter/ttk/dirbrowser.py
(made OOP from the second one)
"""
import os
import tkinter
import tkinter.ttk


class DirectoryBrowser(tkinter.ttk.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)

        self.tree = tkinter.ttk.Treeview(self, columns=("fullpath", "type", "size"),
                                         displaycolumns="", yscrollcommand=lambda f, l: self.autoscroll(self.vsb, f, l),
                                         xscrollcommand=lambda f, l: self.autoscroll(self.hsb, f, l))

        s = tkinter.ttk.Style()
        s.configure("Treeview", background=self["background"],
                    foreground="#BBBBBB")


        self.vsb = tkinter.ttk.Scrollbar(self, orient="vertical")
        self.hsb = tkinter.ttk.Scrollbar(self, orient="horizontal")

        self.vsb['command'] = self.tree.yview
        self.hsb['command'] = self.tree.xview

        self.tree.heading("#0", text="Project", anchor='w')

        self.populate_roots()
        self.tree.bind('<<TreeviewOpen>>', self.update_tree)
        # self.tree.bind('<Double-Button-1>', self.change_dir)

        # Arrange the self.tree and its scrollbars in the toplevel
        self.tree.grid(column=0, row=0, sticky='nswe')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='ew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def populate_tree(self, node):
        if self.tree.set(node, "type") != 'directory':
            return

        path = self.tree.set(node, "fullpath")
        self.tree.delete(*self.tree.get_children(node))

        dirCount = 0

        for p in [elem for elem in os.listdir(path) if elem[0] != '.' and (elem[:2:] != "__" and elem[-2::] != "__")]:
            ptype = None
            p = os.path.join(path, p).replace('\\', '/')
            if os.path.isdir(p):
                ptype = "directory"
            elif os.path.isfile(p):
                ptype = "file"

            fname = os.path.split(p)[1]
            id = self.tree.insert(node, "end", text=fname, values=[p, ptype])

            if ptype == 'directory':
                if fname not in ('.', '..'):
                    self.tree.insert(id, 0, text="dummy")
                    self.tree.item(id, text=fname)
                    self.tree.move(id, self.tree.parent(id), dirCount)
                    dirCount += 1
            elif ptype == 'file':
                size = os.stat(p).st_size
                self.tree.set(id, "size", "%d bytes" % size)

    def populate_roots(self):
        dir = os.path.abspath('.').replace('\\', '/')
        node = self.tree.insert('', 'end', text=dir, values=[dir, "directory"])
        self.populate_tree(node)

    def update_tree(self, event):
        self.tree = event.widget
        self.populate_tree(self.tree.focus())

    def _change_dir(self, event):
        self.tree = event.widget
        node = self.tree.focus()
        if self.tree.parent(node):
            path = os.path.abspath(self.tree.set(node, "fullpath"))
            if os.path.isdir(path):
                os.chdir(path)
                self.tree.delete(self.tree.get_children(''))
                self.populate_roots()

    def autoscroll(self, sbar, first, last):
        """Hide and show scrollbar as needed."""
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)


if __name__ == "__main__":
    root = tkinter.Tk()

    DirectoryBrowser(root).pack(expand=True, fill="both")

    root.mainloop()
