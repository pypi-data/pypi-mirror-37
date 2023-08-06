from .kernel import *
from math import pi

@shape_method
def move(shape, *args):
    if len(args) == 1: args = args[0]
    delta_x = args[0]
    delta_y = args[1]
    delta_z = args[2] if len(args) == 3 else 0
    return shape.remap(x-delta_x, y-delta_y, z-delta_z)

@shape_method
def move_x(shape, delta):
    return shape.remap(x-delta, y, z)

@shape_method
def move_y(shape, delta):
    return shape.remap(x, y-delta, z)

@shape_method
def move_z(shape, delta):
    return shape.remap(x, y, z-delta)

@shape_method
def rotate_x(shape, angle):
    cos_angle = cos(angle*pi*2)
    sin_angle = sin(angle*pi*2)
    return shape.remap(x, cos_angle*y + sin_angle*z, -sin_angle*y + cos_angle*z)

@shape_method
def rotate_y(shape, angle):
    cos_angle = cos(angle*pi*2)
    sin_angle = sin(angle*pi*2)
    return shape.remap(cos_angle*x + sin_angle*z, y, -sin_angle*x + cos_angle*z)

@shape_method
def rotate_z(shape, angle):
    cos_angle = cos(angle*pi*2)
    sin_angle = sin(angle*pi*2)
    return shape.remap(cos_angle*x + sin_angle*y, -sin_angle*x + cos_angle*y, z)
