import math

import numpy as np

from src.geometry.Shape import Shape
from src.geometry.Vector import Vector


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

    def iteratePoints(self, resolution, startAngle=0, endAngle=2 * math.pi):
        for angle in np.arange(0, 2 * math.pi, 2 * math.pi / resolution):
            yield self.pointAtAngle(angle)

    def polyline(self, resolution):
        shape = Shape(
            [
                self.pointAtAngle(angle)
                for angle in np.arange(0, 2 * math.pi, 2 * math.pi / resolution)
            ]
        )
        shape.close()
        return shape


def arc(center: Vector, radius: float, startAngle=0.0, angleSize=2.0 * math.pi):
    circle = Circle(center, radius)
    step = angleSize / 100.0
    shape = Shape()
    for angle in np.arange(startAngle, startAngle + angleSize, step):
        point = circle.pointAtAngle(angle)
        shape.lineTo(point)

    return shape
