
import drawSvg as draw

from geometry.vec2 import vec2


class LineSegment:
    "A line with a start and an end in 2d space"

    start: vec2
    end: vec2

    def __init__(self, start, end):
        if start == end:
            raise ValueError
        self.start = start
        self.end = end

    @property
    def vector(self):
        return self.end - self.start

    @vector.setter
    def vector(self, vector: vec2):
        self.end = self.start + vector

    def unitVector(self):
        return self.vector.unitVector()

    @property
    def direction(self):
        "Alias for unitVector"
        return self.unitVector()

    @property 
    def length(self):
        return self.vector.length

    @length.setter
    def length(self, length: float):
        self.vector = self.vector.withLength(length)

    @property
    def angle(self):
        return self.vector.angle

    @angle.setter
    def angle(self, angle):
        self.vector = self.vector.withAngle(angle)

    def copy(self):
        # TODO: I'll bet copy methods aren't the way!
        return LineSegment(self.start.copy(), self.end.copy())

    def withAngle(self, angle):
        new = self.copy()
        new.angle = angle
        return new

    def withLength(self, length):
        new = self.copy()
        new.length = length
        return new

    def pointAlong(self, lengthAlong) -> vec2:
        if lengthAlong < 0 or lengthAlong > self.length:
            raise ValueError
        else:
            progress = lengthAlong / self.length
            return self.start * (1.0 - progress) + self.end * progress

    def normalAlong(self, lengthAlong):
        start = self.pointAlong(lengthAlong)
        direction = self.direction.normal()
        return LineSegment(start=start, end=start + direction)
        

    def svg(self):
        return draw.Line(self.start.x, self.start.y, self.end.x, self.end.y)

    # Bounding rectangle methods
    @property
    def top(self):
        return max([self.start.y, self.end.y])

    @property
    def bottom(self): 
        return min([self.start.y, self.end.y])
    
    @property
    def left(self): 
        return min([self.start.x, self.end.x])

    @property
    def right(self):
        return max([self.start.x, self.end.x])

    def __str__(self):
        return "{} -> {}".format(self.start, self.end)

    def translate(self, vec):
        return LineSegment(start = self.start + vec, end = self.end + vec)


