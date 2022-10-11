import math

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
        if self.x == 0:
            return 1/2 * math.pi if self.y > 0 else 3/2 * math.pi
        return math.atan(self.y/self.x)
    
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




