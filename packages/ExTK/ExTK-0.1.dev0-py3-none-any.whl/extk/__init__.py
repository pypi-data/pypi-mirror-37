from tkinter.filedialog import askopenfilename
from tkinter import *

# placeholder entry
class Entry(Entry):
    "The modified entry widget with more formatting capabilities and a placeholder option."
    def __init__(self, master=None, placeholder="", color='grey', width=20, password=False, format_type=None):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = "#000000"
        self.width = width
        self.password = password
        self.format_type = format_type

        self['width'] = self.width

        if format_type == 'number':
            self['justify'] = RIGHT

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self['fg'] = self.placeholder_color
        self.insert(0, self.placeholder)

        if self.password:
            self['show'] = ""

        vcmd = (self.register(self.callback))

        self['validate'] = 'all'
        self['validatecommand'] = (vcmd, '%P')

        if self.format_type == 'number':
            self['font'] = "System 13"

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self['fg'] = self.default_fg_color
            self.delete('0', 'end')
            if self.password:
                self['show'] = "•"
            if self.format_type == 'number':
                self['font'] = "Menlo 14"

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def callback(self, P):
        if self['fg'] == self.default_fg_color:
            if self.format_type == "number":
                if str.isdigit(P.replace(".", "").lstrip("-")) or P.lstrip("-") == "":
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True


# file select
class FileSelect(Frame):
    def __init__(self, master=None, button_text="Choose file", dialog={}):
        super().__init__(master)
        self.button = Button(self, text=button_text, command=self.getfile)
        self.label = Label(self, text="No file chosen")
        self.button.pack(side=LEFT)
        self.label.pack(side=RIGHT)
        self.filename = ""
        self.dialog = dialog

    def getfile(self):
        f = askopenfilename(**self.dialog)
        if f != "":
            self.label.config(text=f)
            self.filename = f

if __name__ == "__main__":
    root = Tk()

    extitlelabel = Label(root, text="ExTK Examples", font="System 25 bold").pack()

    exphelabel = Label(root, text="Placeholder Entry", font="System 15 bold").pack()

    username = Entry(root, "username")
    password = Entry(root, "password", password=True)
    number = Entry(root, "number",  format_type="number")

    username.pack()
    password.pack()
    number.pack()

    exfilelabel = Label(root, text="File Chooser", font="System 15 bold").pack()

    file = FileSelect(root)
    file.pack()

    root.mainloop()
