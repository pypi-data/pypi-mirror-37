from types import GeneratorType as generator
from .kernel import *

class Vector(list):

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple, zip, generator)): args = tuple(args[0])
        if len(args) == 2: args = args + (0,)
        super().__init__(args)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def __neg__(self):
        return Vector(-a for a in self)

    def __add__(self, other):
        if isinstance(other, Vector):
            assert len(other) == len(self)
            return Vector(s+o for s,o in zip(self,other))
        elif isinstance(other, (float, int)):
            return Vector(s+other for s in self)

    def __sub__(self, other):
        if isinstance(other, Vector):
            assert len(other) == len(self)
            return Vector(s-o for s,o in zip(self,other))
        elif isinstance(other, (float, int)):
            return Vector(s-other for s in self)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Vector(s*other for s in self)

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Vector(s/other for s in self)

    def __floordiv__(self, other):
        if isinstance(other, (float, int)):
            return Vector(s//other for s in self)

    def dot(self, other):
        assert len(other) == len(self)
        return sum(s*o for s,o in zip(self,other))

    def norm(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
