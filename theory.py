from logic import *  # will import all classes in that document
from constant import *  # will import all classes in that document
from variable import *  # will import all classes in that document
from equation import *  # will import all classes in that document

class Theory(Logic):
    def __init__(self, name, description, equation):   # constructor for class
        self._name = name
        self._description = description
        self._equation = equation

    def get_equation(self):
        return self._equation


# x = Variable("horizontal displacment", "x", None, "meters", "indicates horizontal displacment")
# y = Constant("vertical displacment", "y", 3, "meters", "indicates vertical displacment")
#
# e = Equation("sin", "x+sin(x+y^2)", [x, y], "sine wave")
#
# t = Theory('bob', "its a thingy", e)
#
# print(t.get_description())
# print(t.get_description())
# print(t.get_equation().get_equation_latex())
#
# print(type(t))
# print(isinstance(x, Variable))  # lets you check the type of variable something is
# if type(t) == Variable:
#     print(True)
# else:
#     print(False)
# print(type(t.get_equation()))