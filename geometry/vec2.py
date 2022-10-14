import math
from multimethod import multimethod
from multipledispatch import dispatch
import drawSvg as draw

class vec2:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other) -> None:
        return self.x == other.x and self.y == other.y

    def __mul__(self, scale: float) -> "vec2":
        return vec2(self.x * scale, self.y * scale)

    def __add__(self, other) -> "vec2":
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "vec2": 
        return vec2(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)

    def __truediv__(self, divisor) -> "vec2":
        return self * ( 1 / divisor)


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
        return vec2(self.x, self.y)

    def withAngle(self, angle):
        "Make a new vector with the same length but different angle"
        new = self.copy()
        new.angle = angle
        return new 

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
        return vec2(-self.y, self.x)


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
        return self + vec2(0, -amount)

    @squareDown.register
    def squareDownToPoint(self, point: "vec2"):
        return vec2(self.x, point.y)

    @multimethod    
    def squareUp(self, amount: float):
        return self + vec2(0, amount)

    @squareUp.register
    def squareUpToPoint(self, point: "vec2"):
        return vec2(self.x, point.y)

    @multimethod    
    def squareRight(self, amount: float):
        return self + vec2(amount, 0)

    @squareRight.register
    def squareRightToPoint(self, point: "vec2"):
        return vec2(point.x, self.y)

    @multimethod    
    def squareLeft(self, amount: float):
        return self + vec2(-amount, 0)

    @squareLeft.register
    def squareLeftToPoint(self, point: "vec2"):
        return vec2(point.x, self.y)

    def move(self, x, y):
        new = vec2(self.x + x, self.y +y)
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


    label: str | None = None
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
            label = draw.Text(labelText, 5, self.x + 2, self.y + 2, fill="#000000", stroke="none")
            group.append(label)

        return group


def midpoint(a: vec2, b: vec2):
    return (a + b) * .5
