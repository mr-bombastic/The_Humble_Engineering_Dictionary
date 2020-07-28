from Classes.logic import *  # will import all classes in that document


class Constant(Logic):
    def __init__(self, name, symbol, value, units, description):  # constructor for class
        self._name = str(name)
        self._symbol = str(symbol)
        self._value = value
        self._units = str(units)
        self._description = str(description)

    def get_symbol(self):
        return self._symbol

    def get_value(self):
        return self._value

    def get_units(self):
        return self._units
