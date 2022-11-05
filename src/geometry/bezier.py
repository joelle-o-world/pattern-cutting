from src.geometry.Group import Group
from src.geometry.Shape import Shape, dashed
from src.geometry.Vector import Vector


class BezierCurve:
    def __init__(self, p0: Vector, p1: Vector, p2: Vector, p3: Vector):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def B(self, t):

        return (
            self.p0 * pow(1.0 - t, 3.0)
            + self.p1 * 3 * pow(1 - t, 2) * t
            + self.p2 * 3 * (1 - t) * t * t
            + self.p3 * pow(t, 3.0)
        )

    def points(self, numberOfPoints):
        return [self.B(t / (numberOfPoints - 1)) for t in range(0, numberOfPoints)]

    def shape(self, numberOfPoints):
        return Shape(self.points(numberOfPoints))

    def demo(self):
        return Group(
            self.shape(50),
            *self.points(10),
            dashed(self.p1, self.p0),
            dashed(self.p2, self.p3),
        )
