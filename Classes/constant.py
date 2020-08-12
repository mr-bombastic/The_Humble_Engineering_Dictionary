from Classes.variable import *  # will import all classes in that document


class Constant(Variable):
    def __init__(self, name, symbol, value, units, description, image):  # constructor for class
        super(Constant, self).__init__(name, symbol, units, description, image)

        self._value = value

    def set_value(self):
        pass