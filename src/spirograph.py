from .geometry.Shape import Shape
from .geometry.Vector import polar, Vector
import numpy as np

def spiro(angle_function, length: float, resolution: float = 3):
    shape = Shape().start_at(Vector(0,0))
    for w in np.arange(0, length, resolution):
        last_angle = shape.last_segment.angle if shape.number_of_points > 1 else 0
        angle = last_angle + (angle_function(w) / resolution)
        next_point = shape.last_point + polar(length=resolution, angle=angle)
        shape.line_to(next_point)
    return shape
