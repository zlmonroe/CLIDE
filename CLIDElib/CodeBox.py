if __name__ == "__main__":
    import __fixDir__

import tkinter
import tkinter.font as tkFont
import re
from CLIDElib.ChangeText import ChangeText
import CLIDElib.lispSyntaxLists as lisp
from CLIDElib.tooltip import ToolTip


def any(name, alternates):
    "Return a named group pattern matching list of alternates."
    return "(?P<%s>" % name + "|".join(alternates) + ")"


funcMatchString = r"(?:(?<=[\s()])|^)(" + any("FUNC", lisp.functions + lisp.genericFunctions) + r")(?:(?=[\s()\n])|$)"
funcMatch = re.compile(funcMatchString)
macroMatchString = r"(?:(?<=[\s()])|^)(" + any("FUNC", lisp.macros) + r")(?:(?=[\s()\n])|$)"
macroMatch = re.compile(macroMatchString)
specMatchString = r"(?:(?<=[\s()])|^)(" + any("FUNC", lisp.specialForms) + r")(?:(?=[\s()\n])|$)"
specMatch = re.compile(specMatchString)
typeMatchString = r"(?:(?<=[\s()])|^)(" + any("FUNC", lisp.types) + r")(?:(?=[\s()\n])|$)"
typeMatch = re.compile(typeMatchString)
loopMatchString = r"(?:(?<=[\s()])|^)(" + any("FUNC", lisp.loopClauses) + r")(?:(?=[\s()\n])|$)"
loopMatch = re.compile(loopMatchString)
varMatchString = r"(?:(?<=[\s()])|^)(" + any("FUNC", lisp.variables) + r")(?:(?=[\s()\n])|$)"
varMatch = re.compile(varMatchString)
constMatchString = r"(?:(?<=[\s()])|^)(" + any("FUNC", lisp.constants) + r")(?:(?=[\s()\n])|$)"
constMatch = re.compile(constMatchString)


class CodeBox(ChangeText):
    def __init__(self, *args, **kwargs):
        ChangeText.__init__(self, *args, **kwargs)

        self.deletionFlag = False

        self.font = tkFont.Font(family="Courier", size=12)
        self.fontBold = self.font.copy()
        self.fontBold["weight"] = "bold"
        self.config(font=self.font)

        self.bind("<KeyRelease>", self._keyRelease)
        self.bind("<KeyPress>", self._keyPress)
        self.bind_all("<<Change>>", self._highlightLine)
        self.tag_config("Current Line", background="cornsilk")
        self.tag_lower("Current Line")
        self.tag_config("Open Left Paren", background="#ff9e9e")
        self.tag_config("Open Right Paren", background="#9effaf")
        self.tag_config("Variables", foreground="#66ffff", font=self.fontBold)
        self.tag_config("Constants", foreground="#000099", font=self.fontBold)
        self.tag_config("Comments", foreground="blue")
        self.tag_config("Special Forms", foreground="green", font=self.fontBold)
        self.tag_config("Types", foreground="red", font=self.fontBold)
        self.tag_config("Loop Clauses", foreground="#ff99ff", font=self.fontBold)
        self.tag_config("Macros", foreground="orange", font=self.fontBold)
        self.tag_config("Functions", foreground="#ac00e6", font=self.fontBold)

        self.toolTip = ToolTip(self)

        def post(event):
            # get the index of the mouse click
            index = self.index("insert")
            tags = [tag for tag in self.tag_names(index + " -1c") if tag in ["Open Left Paren", "Open Right Paren", "Comments", "Functions", "Macros", "Special Forms", "Types", "Loop Clauses", "Variables", "Constants"]]
            helpText = ""
            for tag in tags:
                helpText += tag + "\n"
            self.toolTip.showtip(helpText[:-1])
            self.after(3000, self.toolTip.hidetip)
            return "break"

        self.bind("<Alt-Return>", post)

    def _keyRelease(self, event):
        """handles the special events on keypress"""

        # find parenthesis through old fashioned stack style search
        openRight = []
        openLeft = []
        comments = []

        # if keysym is control v, need to set start to 0.0 and end to "end"
        currentIndex = 0
        for char in self.get("1.0", "end"):
            if char == "(":
                openRight.append("0.0 +%sc" % currentIndex)
            elif char == ")":
                if len(openRight) == 0:
                    openLeft.append("0.0 +%sc" % currentIndex)
                else:
                    openRight.pop()
            elif char == ";":
                comments.append("0.0 +%sc" % currentIndex)
            currentIndex += 1

        # uncolor the old tags
        self.tag_remove("Open Left Paren", "1.0", "end")
        self.tag_remove("Open Right Paren", "1.0", "end")
        self.tag_remove("Comments", "1.0", "end")
        self.tag_remove("Functions", "1.0", "end")
        self.tag_remove("Macros", "1.0", "end")
        self.tag_remove("Special Forms", "1.0", "end")
        self.tag_remove("Types", "1.0", "end")
        self.tag_remove("Loop Clauses", "1.0", "end")
        self.tag_remove("Variables", "1.0", "end")
        self.tag_remove("Constants", "1.0", "end")
        # recolor the new
        for index in openLeft:
            self.tag_add("Open Left Paren", index)
        for index in openRight:
            self.tag_add("Open Right Paren", index)
        for index in comments:
            self.tag_add("Comments", index, "%s lineend" % index)
        # find functions/keywords using regex
        for func in funcMatch.finditer(self.get("1.0", "end")):
            self.tag_add("Functions", "1.0 + %dc" % func.start(0), "1.0 + %dc" % func.end(0))
        for macro in macroMatch.finditer(self.get("1.0", "end")):
            self.tag_add("Macros", "1.0 + %dc" % macro.start(0), "1.0 + %dc" % macro.end(0))
        for spec in specMatch.finditer(self.get("1.0", "end")):
            self.tag_add("Special Forms", "1.0 + %dc" % spec.start(0), "1.0 + %dc" % spec.end(0))
        for type in typeMatch.finditer(self.get("1.0", "end")):
            self.tag_add("Types", "1.0 + %dc" % type.start(0), "1.0 + %dc" % type.end(0))
        for loop in loopMatch.finditer(self.get("1.0", "end")):
            self.tag_add("Loop Clauses", "1.0 + %dc" % loop.start(0), "1.0 + %dc" % loop.end(0))
        for var in varMatch.finditer(self.get("1.0", "end")):
            self.tag_add("Variables", "1.0 + %dc" % var.start(0), "1.0 + %dc" % var.end(0))
        for const in constMatch.finditer(self.get("1.0", "end")):
            self.tag_add("Constants", "1.0 + %dc" % const.start(0), "1.0 + %dc" % const.end(0))

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
