from src.geometry.Shape import Shape
from src.geometry.Vector import Vector, polar


class Notch:
    def __init__(self, position: Vector, angle, length, width):
        self.position = position
        self.angle = angle
        self.length = length
        self.width = width

    def direction(self):
        return polar(self.angle, 1)

    @property
    def top(self):
        return self.shape().top

    @property
    def bottom(self):
        return self.shape().bottom

    @property
    def left(self):
        return self.shape().left

    @property
    def right(self):
        return self.shape().right

    def shape(self):
        end = self.position
        start = self.position + self.direction() * self.length
        direction = self.direction()
        perp = direction.normal()
        return Shape(
            [
                start - (perp * self.width * 0.5),
                end - perp * self.width * 0.5,
                end + perp * self.width * 0.5,
                start + (perp * self.width * 0.5),
            ],
            style="notch",
        )

    def svg(self):
        return self.shape().svg()


def notch_on_shape(shape: Shape, where: float | int | Vector, length=10.0, width=3.0):
    at = shape.at(where)
    return Notch(position=at.point, angle=at.normal().angle, length=length, width=width)
