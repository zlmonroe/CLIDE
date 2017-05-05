if __name__ == "__main__":
    import __fixDir__

import tkinter
from CLIDElib.ChangeText import ChangeText


class CodeBox(ChangeText):
    def __init__(self, *args, **kwargs):
        ChangeText.__init__(self, *args, **kwargs)

        self.deletionFlag = False

        self.bind("<KeyPress>", self.keyPress)
        self.bind_all("<<Change>>", self._highlightLine)
        self.tag_config("Current Line", background="cornsilk")

    def keyPress(self, event):
        """handles the special events on keypress"""
        # if the selection includes right paren, don't allow delete
        if self.tag_ranges("sel"):
            lcount = self.selection_get().count(")")
            rcount = self.selection_get().count("(")
            if len(event.keysym) == 1 and (lcount != rcount):
                print(lcount - rcount)
                self.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
                self.insert(tkinter.INSERT, "(" * (rcount - lcount) * (0 if rcount < lcount else 1))
                self.insert(tkinter.INSERT, event.keysym)
                self.insert(tkinter.INSERT, ")" * (lcount - rcount) * (0 if lcount < rcount else 1))
                self.selection_clear()
            return "break"
        elif event.keysym == "Tab":
            self.insert("insert", (4 - len(self.get("insert linestart", "insert")) % 4) * " ")
            return "break"
        # dont backspace right paren, but instead skip over to thing before
        # delete spaces like tabs
        elif event.keysym == "BackSpace":
            char = self.get("insert -1c", "insert")
            if char == ")":
                pos = self.search(r'[^)]', "insert", "1.0", regexp=True, backwards=True)
                if self.get(pos, pos + " +1c") == "(":
                    self.delete("insert -1c", "insert")
                self.mark_set("insert", pos + " +1c")
            elif char == "(":
                nextClose = self.search(")", "insert", stopindex="end")
                self.delete(nextClose, nextClose + " + 1c")
            elif char == " ":
                lastFourChar = self.get("insert -%dc" % (4 - len(self.get("insert linestart", "insert")) % 4), "insert")
                while lastFourChar and lastFourChar[-1] == " ":
                    lastFourChar = lastFourChar[0:-1:1]
                    self.delete("insert -1c", "insert")
                return "break"
        # dont allow delete of right paren
        elif event.keysym == "Delete":
            char = self.get("insert", "insert +1c")
            if char == ")":
                return "break"
            elif char == "(":
                # TODO implement left paren matching delete
                return "break"
        # dont insert right paren, but do skip it
        elif event.keysym == "parenright":
            if self.get("insert", "insert +1c") == ")":
                self.mark_set("insert", "insert +1c")
            return "break"
        # insert both left and right paren and move cursor behind right
        elif event.keysym == "parenleft":
            self.insert("insert", "()")
            self.mark_set("insert", "insert -1c")
            return "break"
        elif event.keysym == "Return":
            if self.get("insert linestart", "insert").strip(" ") == "":
                self.insert("insert", "\n" + self.get("insert linestart", "insert"))
                return "break"

    def _highlightLine(self, event=None):
        """highlights the cursor's line in text widget"""

        self.tag_remove("Current Line", "1.0", tkinter.END)
        if self.tag_ranges("sel") == ():
            self.tag_add("Current Line", "insert linestart", "insert lineend+1c")
        else:
            self.tag_add("Current Line", "insert linestart", "insert lineend+1c")
            ranges = self.tag_ranges("sel")
            self.tag_remove("Current Line", ranges[0], ranges[1])


if __name__ == "__main__":
    root = tkinter.Tk()
    text = CodeBox(root)
    text.pack()
    root.mainloop()
