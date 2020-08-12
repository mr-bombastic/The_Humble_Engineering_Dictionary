from Classes.logic import *  # will import all classes in that document


class Variable(Logic):   # inherits everything from constant (even the constructor)
    def __init__(self, name, symbol, units, description, image):  # constructor for class
        super(Logic, self).__init__(name, description, image)

        self._symbol = str(symbol)
        self._units = str(units)
        self._value = 0

    def get_symbol(self):
        return self._symbol

    def get_value(self):
        return self._value

    def get_units(self):
        return self._units

    def set_value(self, new_value):
        self._value = new_value
