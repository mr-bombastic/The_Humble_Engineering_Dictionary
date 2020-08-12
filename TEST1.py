from tkinter import *
from Classes.logic import *

root = Tk()
canvas = Canvas(root, width = 300, height = 300)
canvas.pack()

L = Logic("name", "desciption", "Dictionary\logic\red.png")

canvas.create_image(20,20, anchor=NW, image=L.get_image())
mainloop()