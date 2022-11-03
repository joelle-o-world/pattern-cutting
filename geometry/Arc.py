from vec2 import vec2
from Shape import Shape
import numpy as np
import math
from render import render


class Arc:
    def __init__(self, center: vec2, radius: float, startAngle: float, endAngle: float):
        self.center = center
        self.radius = radius
        self.startAngle = startAngle
        self.endAngle = endAngle

    def pointAtAngle(self, angle):
        return self.center + vec2(1, 0).withAngle(angle).withLength(self.radius)

    def polyline(self, resolution = 100):
        step = (self.endAngle - self.startAngle) / resolution
        return Shape([self.pointAtAngle(angle) for angle in np.arange(self.startAngle, self.endAngle, step)])


if __name__ == "__main__":
    myArc = Arc(center = vec2(0, 50), radius=20, startAngle = 0, endAngle = math.pi)
    render(myArc.polyline()).saveSvg("Arc example.svg")
