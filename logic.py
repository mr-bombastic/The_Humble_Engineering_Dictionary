class Logic:     # just important for get_name and get_description (means its only written in one place)
    def __init__(self, name, description, image):  # constructor for class
        self._name = name
        self._description = description
        self._image = image

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_image(self):
        return self._image
