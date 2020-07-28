from tkinter import *

window = Tk()  # creates the window

frame = Frame(window)
frame.pack()

val = StringVar()

test1 = Button(frame, text="test")
test2 = Label(frame, text="test")
test3 = Entry(frame)
test4 = Button(frame, text="test")
test5 = Label(frame, text="test")
test6 = OptionMenu(frame, val, "test")

val.set("Variable")

print(test6.getvar("variable"))

for item in frame.winfo_children():
    if item.winfo_class() == "optionMenu":
        print(item.get())


window.mainloop()