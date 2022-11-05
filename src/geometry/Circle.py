import math
import numpy as np
from src.geometry.Vector import Vector
from src.geometry.Shape import Shape


class Circle:
    def __init__(self, center: Vector, radius: float):
        self.center = center
        self.radius = radius

    @property
    def circumference(self):
        return 2 * math.pi * self.radius

    def pointAtAngle(self, angle):
        return self.center + Vector(1, 0).withAngle(angle).withLength(self.radius)

    def pointAlong(self, w):
        angle = w / self.circumference * 2 * math.pi
        return self.pointAtAngle(angle)

    def iteratePoints(self, resolution):
        for angle in np.arange(0, 2 * math.pi, 2 * math.pi / resolution):
            yield self.pointAtAngle(angle)

    def polyline(self, resolution):
        shape = Shape([self.pointAtAngle(angle) for angle in np.arange(0, 2 * math.pi, 2*math.pi / resolution)])
        shape.close()
        return shape



