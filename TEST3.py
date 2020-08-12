class A(object):
    def __init__(self, string):
        print(string + " world")

class B(A):
    def __init__(self, string):
        print(string)
        super(B, self).__init__(string)

B("gfsdh")