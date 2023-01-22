from .geometry.Shape import Shape
from .geometry.Vector import Vector

square = Shape([
    Vector(0,0),
    Vector(0, 100),
    Vector(100, 100),
    Vector(100, 0)
]).close()
