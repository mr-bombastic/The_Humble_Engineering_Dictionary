from matplotlib import *
from matplotlib import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

use('TkAgg')


def graph(text_to_display, fi, can):
    text_to_display = entry.get()
    text_to_display = "$"+text_to_display+"$"

    fi.clear()
    fi.text(0, 0.5, text_to_display, fontsize=50)  # (x coordinat, y coordinat, text, font size)
    can.draw()

root = Tk()

text = StringVar()
entry = Entry(root, textvariable=text)
entry.pack(expand=True)

fig = figure.Figure()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

root.bind('<Return>', lambda e: graph(e, fig, canvas))


root.mainloop()