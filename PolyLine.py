import math
import drawSvg as draw

# TODO: should probable rename as vector
class vec2:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __mul__(self, scale: float):
        return vec2(self.x * scale, self.y * scale)

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other): 
        return vec2(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    @property
    def angle(self):
        if self.x == 0:
            return 1/2 * math.pi if self.y > 0 else 3/2 * math.pi
        return math.atan(self.y/self.x)
    
    @angle.setter
    def angle(self, angle):
        m = self.length
        self.x = math.cos(angle) * m
        self.y = math.sin(angle) * m

    @property
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    @length.setter
    def length(self, length):
        self *= length / self.length



class LineSegment:
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

    @property 
    def length(self):
        return self.vector.length

    @length.setter
    def length(self, length: float):
        self.vector.length = length

    @property
    def angle(self):
        return self.vector.angle

    @angle.setter
    def angle(self, angle):
        self.vector.angle = angle

    def pointAlong(self, lengthAlong):
        if lengthAlong < 0 or lengthAlong > self.length:
            raise ValueError
        else:
            progress = lengthAlong / self.length
            return self.start * (1.0 - progress) + self.end * progress

    # Bounding rectangle methods
    def top(self):
        return max([self.start.y, self.end.y])

    def bottom(self): 
        return min([self.start.y, self.end.y])
    
    def left(self): 
        return min([self.start.x, self.end.x])

    def right(self):
        return max([self.start.x, self.end.x])

    def __str__(self):
        return "{} -> {}".format(self.start, self.end)

class Intersection:
    a: vec2
    b: vec2
    c: vec2

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @property
    def first(self):
        return LineSegment(self.a, self.b)

    @property
    def second(self):
        return LineSegment(self.b, self.c)

    @property
    def angle(self):
        return self.first.angle + math.pi + self.second.angle


class PolyLine:
    points: list[vec2]

    # Constrction
    def __init__(self, points = []):
        self.points = points

    def append(self, p):
        self.points.append(vec2(p.x, p.y))

    def close(self):
        self.append(self.start())

    # Iteration
    def segments(self):
        "Iterate line segments"
        for start, end in zip(self.points, self.points[1:]):
            yield LineSegment(start, end)

    def intersections(self):
        for a,b,c in zip(self.points, self.points[1:], self.points[2:]):
            yield Intersection(a,b,c)

    def angles(self):
        "Iterate all the three point angles"
        # TODO:

    @property
    def length(self):
        "Measure the total length of the poly line"
        sum = 0.0
        for segment in self.segments():
            sum += segment.length
        return sum

    def pointAlong(self, w):
        "Find a point a certain distance along the polyline"
        sum = 0
        for segment in self.segments():
            if sum + segment.length < w:
                sum += segment.length
            else:
                return segment.pointAlong(w - sum)

    def upsample(self):
        "Interpolate between the points to create a new poly line with greater resolution"
        # TODO

    def resample(self):
        "Increase the resolution of the line, but no gaurantee for keeping the original points"
        # TODO

    def proximity(self, p):
        "How close is point, p, from the poly line"
        # TODO

    def tangent(self, w):
        "Get the tangent to the poly line at w millimeters along."
        # TODO

    def findCorners(self, threshholdAngle):
        "Find sharp corners in the line"
        # TODO

    def top(self):
        "y coordinate of the topmost point"
        return max([point.y for point in self.points])

    def bottom(self):
        "y coordinate of the bottom-most point"
        return min([point.y for point in self.points])

    def left(self):
        "x coordinate of the left-most point"
        return min([point.x for point in self.points])

    def right(self):
        "x coordinate of the right-most point"
        return max([point.x for point in self.points])

    def start(self):
        return self.points[0]
    def end(self):
        return self.points[-1]


    # Exporting
    def interleavedCoordinates(self):
        for point in self.points:
            yield point.x
            yield point.y

    def svg(self):
        "drawSvg object representation"
        return draw.Lines(*self.interleavedCoordinates(), close=False);

    def __str__(self):
        points = ["{}".format(point) for point in self.points]
        return " -> ".join(points)


if __name__ == "__main__":
    square = PolyLine([vec2(1,1), vec2(1,100), vec2(100,100), vec2(100,1), vec2(0,0)])
    d = draw.Drawing(1000, 1000, origin='center',  stroke='black', fill='none')

    d.append(square.svg())
    d.saveSvg("example.svg")

    up = vec2(0, 1)
    print(up.angle)
    left = vec2(1,0)
    print(left.angle)
