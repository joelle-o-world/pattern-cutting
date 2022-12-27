import numpy as np
from src.geometry.Shape import Shape
from src.geometry.Group import Group

def seam_lines(a: Shape, b: Shape, interval=30): 
    g = Group()
    for w in np.arange(0, min(a.length, b.length), interval):
        p = a.point_along(w)
        q = b.point_along(w)
        line = Shape([p, q], style="dashed")
        g.append(line)
    return g

