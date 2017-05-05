if __name__ == "__main__":
    import __fixDir__

import io
import sys
import tkinter
from CLIDElib.PseudoFiles import PseudoInputFile

from CLIDElib.ChangeText import ChangeText


class StdIO(ChangeText, io.TextIOWrapper):
    returnFlag = False
    deleteFlag = False

    def __init__(self, root, *args, **kwargs):
        ChangeText.__init__(self, *args, **kwargs)
        io.TextIOWrapper.__init__(self, PseudoInputFile(self, "stdin", "UTF-8"))

        self.root = root
        self.tag_config("immutable", foreground="gray")

        self.unbind_class(ChangeText, "<Control-o>")

        def windowDeletion():
            self.deleteFlag = True
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", windowDeletion)

        def immutable(event):
            if not (self.tag_ranges("sel")):
                if "immutable" in self.tag_names("insert -1c"):
                    return "break"
            else:
                ranges = self.tag_ranges("sel")
                if "immutable" in self.tag_names(ranges[0]):
                    return "break"

        self.bind("<BackSpace>", immutable)
        self.bind("<Delete>", immutable)

        def blockInsert(event):
            if "immutable" in self.tag_names("insert"):
                if event.keysym not in ["Left", "Right", "Up", "Down"] and (event.keysym != "c" and event.state != 4):
                    return "break"

        self.bind("<Key>", blockInsert)

        self.bind("<Return>", self.returnFlag)

    def isatty(self):
        return True

    def write(self, string):
        immutable = self.tag_ranges("immutable")
        if immutable == ():
            immutable = "1.0"
        else:
            immutable = immutable[1]
        self.insert("%s +1c" % immutable, string, "immutable")
        self.mark_set("insert", "end")
        self.see("end")

    def returnFlag(self, event):
        self.returnFlag = True

    def read(self):
        return self.readline()

    def readline(self):
        self.returnFlag = False
        self.root.update()
        while not self.returnFlag:
            if self.deleteFlag:
                return "\n"
            else:
                self.root.update()
        ranges = self.tag_ranges("immutable")
        if len(ranges) > 1:
            start = ranges[1]
        else:
            start = "1.0"
        read = self.get(start, "insert lineend -1c")
        if read == "":
            read = "\r\n"
        self.tag_add("immutable", start, "insert lineend")
        return read

    def close(self):
        self.process.kill()

    def fileno(self):
        return 0


if __name__ == "__main__":
    root = tkinter.Tk()
    text = StdIO(root)
    text.pack()
    sys.stdin = text
    root.update()
    print(input(""))
    root.mainloop()
