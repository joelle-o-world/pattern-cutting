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


class LineSegment:
    start: vec2
    end: vec2

    def __init__(self, start, end):
        if start == end:
            raise ValueError
        self.start = start
        self.end = end

    def length(self):
        return math.sqrt(math.pow(self.start.x - self.end.x, 2) + math.pow(self.start.y - self.end.y, 2))

    def pointAlong(self, lengthAlong):
        if lengthAlong < 0 or lengthAlong > self.length:
            raise ValueError
        else:
            progress = lengthAlong / self.length()
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

class PolyLine:
    points: list[vec2]
    def __init__(self, points = []):
        self.points = points


    def segments(self):
        "Iterate line segments"
        for start, end in zip(self.points, self.points[1:]):
            yield LineSegment(start, end)

    def angles(self):
        "Iterate all the three point angles"
        # TODO:

    def length(self):
        "Measure the total length of the poly line"
        sum = 0.0
        for segment in self.segments():
            sum += segment.length()
        return sum

    def pointAlong(self, w):
        "Find a point a certain distance along the polyline"
        sum = 0
        for segment in self.segments():
            if sum + segment.length() < w:
                sum += segment.length()
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

    def interleavedCoordinates(self):
        for point in self.points:
            yield point.x
            yield point.y

    def svg(self):
        "drawSvg object representation"
        return draw.Lines(*self.interleavedCoordinates(), close=False);


if __name__ == "__main__":
    square = PolyLine([vec2(1,1), vec2(1,100), vec2(100,100), vec2(100,1), vec2(0,0)])
    d = draw.Drawing(1000, 1000, origin='center',  stroke='black', fill='none')

    d.append(square.svg())
    d.saveSvg("example.svg")
