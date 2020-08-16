from tkinter import *


class Logic:
    def __init__(self, name, description, image):  # constructor for class
        self._name = name
        self._description = description
        self._fields = None

        try:
            self._image = PhotoImage(file="Dictionary/all_images/" + image)
            self._image_local = image

        except:  # this is in case the code cannot find the picture
            self._image = PhotoImage(file="error.png")
            self._image_local = "No image association"

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_image(self):
        return self._image

    def get_image_location(self):
        return self._image_local

    def get_fields(self):
        return self._fields
