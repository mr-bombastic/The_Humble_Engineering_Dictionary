from Classes.variable import *  # will import all classes in that document


class Constant(Variable):
    def __init__(self, name, description, image, symbol, value, units):  # constructor for class
        super().__init__(name, description, image, symbol, units)

        self._value = value

    def set_value(self):
        pass