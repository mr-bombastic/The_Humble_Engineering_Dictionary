from constant import *  # will import all classes in that document


class Variable(Constant):   # inherits everything from constant (even the constructor)

    def set_value(self, new_value):
        self._value = new_value
