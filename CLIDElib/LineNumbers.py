if __name__ == "__main__":
    import __fixDir__

import tkinter


class LineNumbers(tkinter.Frame):
    def __init__(self, root, changeText, *args, **kwargs):
        tkinter.Frame.__init__(self, root, *args, **kwargs)

        self.text = changeText

        self.lineNumbers = tkinter.Canvas(self, width=30)
        self.lineNumbers.pack(expand=True, fill="both")

        self.text.bind("<<Change>>", self.__updateLineNumbers)

    def __updateLineNumbers(self, event):
        """redraw line numbers"""

        cursorline = self.text.index("insert").split(".")[0]
        self.lineNumbers.delete("all")
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            if linenum == cursorline:
                self.lineNumbers.create_rectangle(0, y, 100, y + dline[4] + 5, fill="cornsilk", outline="cornsilk")
            self.lineNumbers.create_text(2, y, anchor="nw", text=linenum)
            i = self.text.index("%s+1line" % i)

if __name__ == "__main__":
    from CLIDElib.ChangeText import ChangeText

    root = tkinter.Tk()
    text = ChangeText(root)
    text.pack(side=tkinter.RIGHT)
    lines = LineNumbers(text)
    lines.pack(side=tkinter.LEFT, expand = True, fill="y")
    root.mainloop()
