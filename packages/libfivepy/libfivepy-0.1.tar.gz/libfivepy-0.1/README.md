# libfivepy

A python library for creating 2D and 3D models.

Libfivepy is based on the amazing [libfive](https://libfive.com/) !


```python
from shapes import *

u = 19
s = 14
t = 3

def key(size):
    return (rectangle(u, u*size) ^ rectangle(s)).move(u/2, (u*size)/2)

def row(*keys):
    if len(keys) == 1: keys = keys[0]
    result = void()
    dy = 0
    for k in keys:
        result |= key(k).move_y(dy)
        dy += k*u
    return result

def keyboard(*rows):
    if len(rows) == 1: rows = rows[0]
    result = void()
    for i,r in enumerate(rows):
        result |= row(r).move_x(i*u)
    return result

full = keyboard([1]*15,[1.5]+[1]*12+[1.5],[2]+[1]*11+[2],[2.5]+[1]*10+[2.5],[1.5,1.5,2,5,2,1.5,1.5])
cutout = bounded_rectangle(u*5,u*8)^bounded_rectangle(u,u*7.5,u*2,u*8)^bounded_rectangle(u*3,u*7.5,u*4,u*8) 
left = full & cutout
right = full ^ cutout

out = full
out = out.extrude_center(t)

region = Region3((-10,200),(-10, 400),(-10, 10))
out.save_mesh(region, 10, "out.stl")
```
