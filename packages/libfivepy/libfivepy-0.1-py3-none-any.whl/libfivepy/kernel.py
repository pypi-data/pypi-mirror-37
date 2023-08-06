from ctypes import *
import math

libfive = cdll.LoadLibrary("/usr/local/lib/libfive.so")

# This section is just to correctly expose the stuct and functions of libfive.h

class Interval(Structure):
    _fields_ = [("lower", c_float), ("upper", c_float)]

class Region2(Structure):
    _fields_ = [("X", Interval), ("Y", Interval)]

class Region3(Structure):
    _fields_ = [("X", Interval), ("Y", Interval), ("Z", Interval)]

class MeshCoords(Structure):
    _fields_ = [("verts", c_void_p), ("vert_count", c_uint32), ("coord_indices", c_void_p), ("coord_index_count", c_uint32)]

libfive.libfive_opcode_enum.argtypes = [c_char_p]
libfive.libfive_opcode_enum.restype = c_int

libfive.libfive_tree_x.argtypes = []
libfive.libfive_tree_x.restype = c_void_p

libfive.libfive_tree_y.argtypes = []
libfive.libfive_tree_y.restype = c_void_p

libfive.libfive_tree_z.argtypes = []
libfive.libfive_tree_z.restype = c_void_p

libfive.libfive_tree_const.argtypes = [c_float]
libfive.libfive_tree_const.restype = c_void_p

libfive.libfive_tree_unary.argtypes = [c_int, c_void_p]
libfive.libfive_tree_unary.restype = c_void_p

libfive.libfive_tree_binary.argtypes = [c_int, c_void_p, c_void_p]
libfive.libfive_tree_binary.restype = c_void_p

libfive.libfive_tree_delete.argtypes = [c_void_p]
libfive.libfive_tree_delete.restype = c_void_p

libfive.libfive_tree_print.argtypes = [c_void_p]
#libfive.libfive_tree_print.restype = POINTER(c_char)

libfive.libfive_tree_remap.argtypes = [c_void_p, c_void_p, c_void_p]
libfive.libfive_tree_remap.restype = c_void_p

libfive.libfive_tree_save_mesh.argtypes = [c_void_p, Region3, c_float, c_char_p]
libfive.libfive_tree_save_mesh.restype = c_bool

#libfive.libfive_tree_render_mesh_coords.argtypes = [c_void_p, Region3, c_float]
#libfive.libfive_tree_render_mesh_coords.restype = POINTER(MeshCoords)

# The main class

class Shape:

    # Constructor

    def __init__(self, ptr):
        self.ptr = ptr

    # Unary operators

    def __neg__(self):
        return unary("neg", self)

    def __invert__(self):
        return unary("recip", self)

    def __abs__(self):
        return unary("abs", self)

    # Binary operators

    def __add__(self, other):
        return binary("add", self, other)

    def __sub__(self, other):
        return binary("sub", self, other)

    def __mul__(self, other):
        return binary("mul", self, other)

    def __truediv__(self, other):
        return binary("div", self, other)

    def __pow__(self, other):
        if other == 2:
            return unary("square", self)
        return binary("pow", self, other)

    # Reverse binary operators

    def __radd__(self, other):
         return  self + other

    def __rsub__(self, other):
         return -self + other

    def __rmul__(self, other):
         return  self * other

    def __rtruediv__(self, other):
         return ~self * other

    # Comparators

    def __gt__(self, other):
        return libfive.libfive_tree_binary(opcode_enum("compare"), self.ptr, other.ptr) == 1

    def __lt__(self, other):
        return libfive.libfive_tree_binary(opcode_enum("compare"), self.ptr, other.ptr) == -1

    # Representation

    def __repr__(self):
        c_result = libfive.libfive_tree_print(self.ptr)
        result = cast(c_result, c_char_p).value.decode()
        libfive.free(c_result)
        return result

    # Destructor

    def __del__(self):
         libfive.libfive_tree_delete(self.ptr)

    # Other functions

    def remap(self, shape_x, shape_y, shape_z):
        return Shape(libfive.libfive_tree_remap(self.ptr, shape_x.ptr, shape_y.ptr, shape_z.ptr))

    def save_mesh(self, region, resolution, file_name):
        return libfive.libfive_tree_save_mesh(self.ptr, region, resolution, file_name.encode())

    def render_mesh_coords(self, region, resolution):
        pass
        #return libfive.libfive_tree_render_mesh_coords(self.ptr, region, resolution)

# Useful functions

def opcode_enum(opcode):
     return libfive.libfive_opcode_enum(str.encode(opcode))

def const_shape(const):
    return Shape(libfive.libfive_tree_const(const))

# Unary functions

def unary(op, a):
    # if isinstance(a, (float, int)): a = const_shape(a)
    return Shape(libfive.libfive_tree_unary(opcode_enum(op), a.ptr))

def sqrt(a):
     if isinstance(a, Shape): return unary("sqrt", a)
     return math.sqrt(a)

def cos(a):
     if isinstance(a, Shape): return unary("cos", a)
     return math.cos(a)

def sin(a):
     if isinstance(a, Shape): return unary("sin", a)
     return math.sin(a)

def tan(a):
     if isinstance(a, Shape): return unary("tan", a)
     return math.tan(a)

def asin(a):
     if isinstance(a, Shape): return unary("asin", a)
     return math.asin(a)

def acos(a):
     if isinstance(a, Shape): return unary("acos", a)
     return math.acos(a)

def atan(a):
     if isinstance(a, Shape): return unary("atan", a)
     return math.atan(a)

def exp(a):
     if isinstance(a, Shape): return unary("exp", a)
     return math.exp(a)

def log(a):
     if isinstance(a, Shape): return unary("log", a)
     return math.log(a)

# Binary functions

def binary(op, a, b):
    if isinstance(a, (float, int)): a = const_shape(a)
    if isinstance(b, (float, int)): b = const_shape(b)
    return Shape(libfive.libfive_tree_binary(opcode_enum(op), a.ptr, b.ptr))

def maximum(*args):
    # return if only one argument or create a nice list
    if len(args) == 1:
        try: args = list(args[0])
        except: return args[0]

    # use libfive only if the list contains a Shape object
    for a in args:
        if isinstance(a, Shape):
            if len(args) == 1: return args[0]
            if len(args) == 2: return binary("max", args[0], args[1])
            return maximum(args[0], maximum(*args[1:]))

    return min(*args)

def minimum(*args):
    # return if only one argument or create a nice list
    if len(args) == 1:
        try: args = list(args[0])
        except: return args[0]

    # use libfive only if the list contains a Shape object
    for a in args:
        if isinstance(a, Shape):
            if len(args) == 1: return args[0]
            if len(args) == 2: return binary("min", args[0], args[1])
            return minimum(args[0], minimum(*args[1:]))

    return min(*args)

# Decorators to add methods to Shape

def shape_method(method):
    setattr(Shape, method.__name__, method)
    return method

# Base coordinates

x = Shape(libfive.libfive_tree_x())
y = Shape(libfive.libfive_tree_y())
z = Shape(libfive.libfive_tree_z())
