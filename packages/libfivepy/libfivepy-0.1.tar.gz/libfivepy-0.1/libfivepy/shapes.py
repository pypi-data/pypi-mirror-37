from .vector import *
from .transforms import *
from .cgs import *

def void():
    return 1

def space():
    return -1

# 2D shapes

def circle(diameter):
    return sqrt(x**2 + y**2) - diameter/2

def bounded_rectangle(*args):
    if len(args) == 4: x0, y0, x1, y1 = args
    elif len(args) == 2: x0, y0, x1, y1 = 0, 0, *args
    elif len(args) == 1: x0, y0, x1, y1 = 0, 0, args[0], args[0]
    return maximum((x0-x), (x-x1), (y0-y), (y-y1))

def rectangle(width, height = None):
    if height == None: height = width
    return maximum((-width/2-x), (x-width/2), (-height/2-y), (y-height/2))

def rounded_rectangle(width, height = None, corner_radius = 1):
    if height == None: height = width
    a = width - corner_radius*2
    b = height - corner_radius*2
    r = rectangle(width, b) | rectangle(a, height)
    for c in [-a/2,a/2]: 
        for d in [-b/2, b/2]:
            r |= circle(corner_radius*2).move(c,d) 
    return r

def exact_rectangle(width, height = None):
    if height == None: height = width
    d = Vector(abs(x) - width/2, abs(y) - height/2)
    return minimum(maximum(d.x, d.y), 0) + Vector(maximum(d.x, 0), maximum(d.y, 0)).norm()

def exact_bounded_rectangle(*args):
    if len(args) == 4: x0, y0, x1, y1 = args
    elif len(args) == 2: x0, y0, x1, y1 = 0, 0, *args
    elif len(args) == 1: x0, y0, x1, y1 = 0, 0, args[0], args[0]
    return exact_rectangle(abs(x1-x0), abs(y1-y0)).move((x0+x1)/2, (y0+y1)/2)

def exact_rounded_rectangle(width, height = None, corner_radius = 1):
    if height == None: height = width
    return exact_rectangle(width - corner_radius*2, height - corner_radius*2) - corner_radius

def polygon(diameter, sides):
    return intersection((x-diameter/2).rotate_z(i/sides) for i in range(sides))

def triangle(diameter):
    return polygon(diameter, 3)

def pentagone(diameter):
    return polygon(diameter, 5)

def hexagone(diameter):
    return polygon(diameter, 6)

# 3D sphapes

def sphere(diameter):
    return sqrt(x**2 + y**2 + z**2) - diameter/2

def bounded_box(point_a, point_b):
    return maximum((point_a.x-x), (x-point_b.x), (point_a.y-y), (y-point_b.y), (point_a.z-z), (z-point_b.z))

def box(width, height = None, depth = None):
    if height == None: height = width
    if depth == None: depth = height
    return bounded_box(Vector(-width/2,-height/2, -depth/2), Vector(width/2, height/2, depth/2))

def cylinder(diameter, *args):
    return circle(diameter).extrude(*args)
