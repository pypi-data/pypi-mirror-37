from .kernel import *

# Basic operations

def union(*args):
    return minimum(*args)
Shape.__or__ = union
Shape.__ror__ = union

def intersection(*args):
    return maximum(*args)
Shape.__and__ = intersection
Shape.__rand__ = intersection

def difference(shape_a, *other_shapes):
    return intersection(shape_a, inverse(union(*other_shapes)))
Shape.__xor__ = difference

def inverse(shape):
    return -shape

def offset(shape, offset):
    return shape - offset

def clearance(shape_a, shape_b, clearance):
    return difference(shape_a, offset(shape_b, clearance))

def shell(shape, shell):
    return clearance(shape, shape, -shell)

def blend_expt(a, b, m):
    return -log(exp(-m*a) + exp(-m*b))/m

# 2D to 3D operations

@shape_method
def extrude(shape, zmin = 1, zmax = 0):
    if zmax == 0 and zmin > 0: zmin, zmax = 0, zmin
    return maximum(shape, zmin-z, z-zmax)

@shape_method
def extrude_center(shape, lenght = 1):
    return maximum(shape, -lenght/2-z, z-lenght/2)

def simple_loft(shape_a, shape_b, zmin, zmax):
    l = (shape_b*(z-zmin) + shape_a*(zmax-z))
    return extrude(l, zmin, zmax)

def loft(shape_a, shape_b, lower, upper):
    def f(z): return (z-lower.z) / (upper.z-lower.z)
    def g(z): return (upper.z-z) / (upper.z-lower.z)
    return simple_loft(shape_a.remap(x+f(z)*(lower.x-upper.x), y+f(z)*(lower.y-upper.y), z),
                       shape_b.remap(x+g(z)*(upper.x-lower.x), y+g(z)*(upper.y-lower.y), z),
                       lower.z, upper.z)
