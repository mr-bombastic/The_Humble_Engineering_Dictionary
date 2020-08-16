import tkinter as tk
from threading import Thread
from time import sleep

def print_hello():
    print("Hello")
    sleep(3)
    print("Done")

root = tk.Tk()

container = tk.Frame(root)
container.pack(fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

frame_main = tk.Frame(container)
frame_main.grid(row=0, column=0, sticky="NSEW")

button_hello = tk.Button(frame_main, text="Say Hello", command=lambda: Thread(target=print_hello).start())
button_hello.grid(sticky="NSEW")
root.mainloop()