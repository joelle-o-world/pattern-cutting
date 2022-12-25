import math

import drawSvg as draw
from multimethod import multimethod


class Vector:
    x: float
    y: float
    label: str | None

    def __init__(self, x, y, label=None):
        self.x = x
        self.y = y
        self.label = label

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __mul__(self, scale: float) -> "Vector":
        return Vector(self.x * scale, self.y * scale)

    def scale_horizontally(self, scalefactor):
        return Vector(self.x * scalefactor, self.y, label=self.label)

    def scale_vertically(self, scalefactor):
        return Vector(self.x, scalefactor * self.y, label=self.label)

    def __add__(self, other) -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)

    def __truediv__(self, divisor: float) -> "Vector":
        return self * (1 / divisor)

    @property
    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    @angle.setter
    def angle(self, angle: float):
        m = self.length
        self.x = math.cos(angle) * m
        self.y = math.sin(angle) * m

    @property
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    @length.setter
    def length(self, length):
        scale = length / self.length
        self.x *= scale
        self.y *= scale

    def unitVector(self):
        return self / self.length

    @property
    def direction(self):
        return self.unitVector()

    def copy(self):
        return Vector(self.x, self.y)

    def with_label(self, label: str):
        return Vector(self.x, self.y, label=label)

    def with_angle(self, angle):
        "Make a new vector with the same length but different angle"
        new = self.copy()
        new.angle = angle
        return new

    def withAngle(self, angle):
        "deprecated alias to with_angle"
        return self.with_angle(angle)

    def withLength(self, length):
        "Make a new vector with the same angle but different length"
        new = self.copy()
        new.length = length
        return new

    def rotate(self, rotation):
        return self.withAngle(self.angle + rotation)

    def extend(self, extension):
        return self.withLength(self.length + extension)

    def normal(self):
        "Get a vector perpendicular to this one"
        # TODO: what about the normal in the other direction?
        return Vector(-self.y, self.x)

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x

    @multimethod
    def squareDown(self, amount: float):
        return self + Vector(0, -amount)

    @squareDown.register
    def squareDownToPoint(self, point: "Vector"):
        return Vector(self.x, point.y)

    @multimethod
    def squareUp(self, amount: float):
        return self + Vector(0, amount)

    @squareUp.register
    def squareUpToPoint(self, point: "Vector"):
        return Vector(self.x, point.y)

    @multimethod
    def squareRight(self, amount: float):
        return self + Vector(amount, 0)

    @squareRight.register
    def squareRightToPoint(self, point: "Vector"):
        return Vector(point.x, self.y)

    @multimethod
    def squareLeft(self, amount: float):
        return self + Vector(-amount, 0)

    @squareLeft.register
    def squareLeftToPoint(self, point: "Vector"):
        return Vector(point.x, self.y)

    def move(self, x, y):
        new = Vector(self.x + x, self.y + y)
        new.label = self.label
        return new

    def moveLeft(self, amount: float):
        return self.move(-amount, 0)

    def moveRight(self, amount: float):
        return self.move(amount, 0)

    def moveUp(self, amount: float):
        return self.move(0, amount)

    def moveDown(self, amount: float):
        return self.move(0, -amount)

    def labelText(self):
        # TODO: automatically add coordinates if flag is set
        return self.label

    def svg(self):
        group = draw.Group()
        circle = draw.Circle(self.x, self.y, 1, fill="black")
        group.append(circle)
        labelText = self.labelText()
        if labelText:
            # TODO: Get font size from a context object
            label = draw.Text(
                labelText, 12, self.x + 2, self.y + 2, fill="#000000", stroke="none"
            )
            group.append(label)

        return group

    @property
    def tuple(self):
        return self.x, self.y


def midpoint(*points):
    summed = Vector(0, 0)
    for point in points:
        summed = summed + point
    return summed / len(points)


def distance(a: Vector, b: Vector):
    return (a - b).length

def polar(angle, length):
    return Vector(length,0).with_angle(angle)
