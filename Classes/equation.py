from Equation import Expression
from Classes.logic import *  # will import all classes in that document


class Equation(Logic):

    def __init__(self, name, description, image, fields, expression, variables):   # constructor for class
        super().__init__(name, description, image, fields)

        self._variables = variables
        self._num_of_var = len(variables)    # stores number of UNIQUE variables
        self._expression = expression

        # extracts the variable's symbol so that it can be placed into the equation
        var_symbols = []
        for i in range(0, len(variables)):
            var_symbols.append(variables[i].get_symbol())

        # puts the given info into the equation library
        # var_symbols is necessary so you can ensure your assigning the correct values to variables
        self._equ = Expression(expression, var_symbols)

    def get_equation_latex(self):   # will return latex version of equation
        return self._expression

    def get_equation_normal(self):   # will return the normal version of equation
        return self._equ.__repr__()

    def get_all_variables(self):    # gives back every variable/constant in equation
        return self._variables

    def get_num_of_variables(self):     # returns number of UNIQUE variables
        return self._num_of_var

    def compile_expression(self):
        pass

    # Will try to solve the array automatically. If a variable doesn't have a value then the user will be asked
    def solve_equation_auto(self):
        values = []     # will store the values of the variables
        for i in range(0, self._num_of_var):     # will go through each variable
            if self._variables[i].get_value() == None:   # when there is no value attached to the variable ask the user
                self._variables[i].set_value(int(input("What is the value for variable " + self._variables[i].get_name() +
                                                  " [" + self._variables[i].get_symbol() + "]?")))
            values.append(self._variables[i].get_value())    # saves the value of the variable

        # the * unpacks the array into its constituent parts so that they can be inputed as individual arguments
        return self._equ(*values)

    def solve_equation_manual(self, values):   # takes array with corresponding user values and solves the equation
        # the * unpacks the array into its constituent parts so that they can be inputed as individual arguments
        return self._equ(*values)
