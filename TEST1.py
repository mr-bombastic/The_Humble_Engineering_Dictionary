import tkinter as tk

def addValuesListBox(listbox):
    for i in range(10):
        listbox.insert(tk.END, i)

def removeValue(event):
    selection = listbox.curselection()
    print(selection)
    listbox.delete(selection)
    print("remove value")

if __name__ == '__main__':
    window = tk.Tk()
    listbox = tk.Listbox(window)
    addValuesListBox(listbox)
    listbox.bind( "<Double-Button-1>" , removeValue )
    listbox.pack()
    window.mainloop()