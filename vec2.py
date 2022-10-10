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

    def __truediv__(self, divisor):
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
        self *= length / self.length

    def unitVector(self):
        return self / self.length 



