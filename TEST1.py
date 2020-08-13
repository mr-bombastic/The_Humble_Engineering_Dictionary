from tkinter import *
from Classes.variable import *

root = Tk()
canvas = Canvas(root, width = 300, height = 300)
canvas.pack()

L = Variable("name", "desciption", "Dictionary\logic\\red.png", "r", "s/m")

canvas.create_image(20,20, anchor=NW, image=L.get_image())
mainloop()