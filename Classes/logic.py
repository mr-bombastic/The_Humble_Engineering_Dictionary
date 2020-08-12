from tkinter import *


class Logic:
    def __init__(self, name, description, image):  # constructor for class
        self._name = name
        self._description = description

        if image:
            try:
                self._image = PhotoImage(file=image)

            except:     # this is in case the code cannot find the picture
                self._image = PhotoImage(file="error.png")

        else:
            self._image = False

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_image(self):
        return self._image
