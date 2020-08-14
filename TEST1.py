from tkinter import *
window = Tk()

def button():
    image = PhotoImage(file="Dictionary/all_latex_images/bar{R}.png")
    lbl = Label(window, image=image)
    lbl.image = image
    lbl.pack()

    canv_image = Canvas(window, width=image.width(), height=image.height(), bg="green")
    canv_image.create_image(0.5, 0.5, anchor="nw", image=image)
    canv_image.pack()

Button(window, command=button, text="press").pack()

window.mainloop()