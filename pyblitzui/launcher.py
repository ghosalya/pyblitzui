from tkinter import Tk, Label, Entry

from script_loader import load_script

FUNCTION_LIST = load_script("blitz_ui.py")

root = Tk()

w = Label(root, text="Welcome to BlitzUI!").grid(row=0)
w = Label(root, text="Loaded file: blitz_ui.py").grid(row=1)

y = 0
for i in range(len(FUNCTION_LIST)):
    function = FUNCTION_LIST[i]
    w = Label(root, text=function["name"]).grid(row=2+y, column=0)
    y += 1
    for argname, argtype in function["args"].items():
        w = Label(root, text=argname).grid(row=2+y, column=0)
        g = Entry(root).grid(row=2+y, column=1)
        y += 1


root.mainloop()