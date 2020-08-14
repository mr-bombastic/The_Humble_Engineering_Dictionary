from Classes.logic import *  # will import all classes in that document


class Method(Logic):
    def __init__(self, name, description, image, steps):  # constructor for class
        super().__init__(name, description, image)

        self._steps = steps

    def get_step(self, i):
        if i < len(self._steps):
            return self._steps[i]
        else:
            return False

    def get_num_steps(self):
        return len(self._steps)

    def get_steps(self):
        return self._steps
