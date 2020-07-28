import tkinter as tk
from tkinter import messagebox

def messagebox_askokcancel():
    if messagebox.askokcancel(title="title", message="message"):
        print("True")
    else:
        print("False")

def messagebox_askquestion():
    if messagebox.askquestion(title="title", message="message"):
        print("True")
    else:
        print("False")

def messagebox_askretrycancel():
    if messagebox.askretrycancel(title="title", message="message"):
        print("True")
    else:
        print("False")

def messagebox_askyesno():
    if messagebox.askyesno(title="title", message="message"):
        print("True")
    else:
        print("False")


def messagebox_askyesnocancel():
    if messagebox.askyesnocancel(title="title", message="message"):
        print("True")
    else:
        print("False")


def messagebox_showerror():
    if messagebox.showerror(title="title", message="message"):
        print("True")
    else:
        print("False")


def messagebox_showinfo():
    if messagebox.showinfo(title="title", message="message"):
        print("True")
    else:
        print("False")


def messagebox_showwarning():
    if messagebox.showwarning(title="title", message="message"):
        print("True")
    else:
        print("False")


tk.Button(text='messagebox_askokcancel', command=messagebox_askokcancel).pack()
tk.Button(text='messagebox_askquestion', command=messagebox_askquestion).pack()
# tk.Button(text='messagebox_askretrycancel', command=messagebox_askretrycancel).pack()
tk.Button(text='messagebox_askyesno', command=messagebox_askyesno).pack()
# tk.Button(text='messagebox_askyesnocancel', command=messagebox_askyesnocancel).pack()
# tk.Button(text='messagebox_showerror', command=messagebox_showerror).pack()
# tk.Button(text='messagebox_showinfo', command=messagebox_showinfo).pack()
# tk.Button(text='messagebox_showwarning', command=messagebox_showwarning).pack()

tk.mainloop()
