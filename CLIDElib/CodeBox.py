if __name__ == "__main__":
    import __fixDir__

import tkinter
from CLIDElib.ChangeText import ChangeText


class CodeBox(ChangeText):
    def __init__(self, *args, **kwargs):
        ChangeText.__init__(self, *args, **kwargs)

        self.deletionFlag = False

        self.bind("<KeyRelease>", self._keyRelease)
        self.bind("<KeyPress>", self._keyPress)
        self.bind_all("<<Change>>", self._highlightLine)
        self.tag_config("Current Line", background="cornsilk")
        self.tag_lower("Current Line")
        self.tag_config("Open Left Paren", background="#ff9e9e")
        self.tag_config("Open Right Paren", background="#9effaf")
        self.tag_config("Comments", foreground="blue")

    def _keyRelease(self, event):
        """handles the special events on keypress"""
        openRight = []
        openLeft = []
        comments = []

        # if keysym is control v, need to set start to 0.0 and end to "end"
        currentIndex = 0
        for char in self.get("1.0", "end"):
            if char == "(":
                # if len(openLeft) == 0:
                openRight.append("0.0 +%sc"%currentIndex)
                # else:
                #     openLeft.pop()
            elif char == ")":
                if len(openRight) == 0:
                    openLeft.append("0.0 +%sc"%currentIndex)
                else:
                    openRight.pop()
            elif char == ";":
                comments.append("0.0 +%sc" % currentIndex)
            currentIndex += 1

        self.tag_remove("Open Left Paren", "1.0", "end")
        self.tag_remove("Open Right Paren", "1.0", "end")
        self.tag_remove("Comments", "1.0", "end")
        for index in openLeft:
            self.tag_add("Open Left Paren", index)
        for index in openRight:
            self.tag_add("Open Right Paren", index)
        for index in comments:
            self.tag_add("Comments", index, "%s lineend"%index)

    def _keyPress(self, event):
        """handles the special events on keypress"""
        if event.keysym == "Tab":
            self.insert("insert", (4 - len(self.get("insert linestart", "insert")) % 4) * " ")
            return "break"
        # delete spaces like tabs
        elif event.keysym == "BackSpace":
            char = self.get("insert -1c", "insert")
            if char == " ":
                lastFourChar = self.get("insert -%dc" % (4 - len(self.get("insert linestart", "insert")) % 4), "insert")
                while lastFourChar and lastFourChar[-1] == " ":
                    lastFourChar = lastFourChar[0:-1:1]
                    self.delete("insert -1c", "insert")
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

    def insert(self, index, chars, *args):
        self.tk.call((self._w, 'insert', index, chars) + args)
        self._keyRelease(tkinter.Event())

    def replace(self, index1, index2, chars, *args):
        self.tk.call(self._w, 'replace', index1, index2, chars, *args)
        self._keyRelease(tkinter.Event())

if __name__ == "__main__":
    root = tkinter.Tk()
    text = CodeBox(root)
    text.pack()
    root.mainloop()
