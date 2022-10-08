import math

class Point:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y


class LineSegment:
    start: Point
    end: Point

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def length(self):
        return math.sqrt(math.pow(self.start.x - self.end.x, 2) + math.pow(self.start.y - self.end.y, 2))


class PolyLine:
    points: list[Point]
    def __init__(self):
        self.points = []

    def segments(self):
        "Iterate line segments"
        list = []
        for start, end in zip(self.points, self.points[1:]):
            list.append(LineSegment(start, end))
        return list

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
        # TODO

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

    def findCorners(self):
        "Find sharp corners in the line"
        # TODO

    def top(self):
        "y coordinate of the topmost point"
        # TODO:

    def bottom(self):
        "y coordinate of the bottom-most point"
        # TODO:

    def left(self):
        "x coordinate of the left-most point"
        #TODO: 

    def right(self):
        "x coordinate of the right-most point"
        # TODO:

    def svg(self):
        "drawSvg object representation"
        # TODO:
