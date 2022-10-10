import math
import drawSvg as draw

from vec2 import vec2
from LineSegment import LineSegment
from Intersection import Intersection

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
        for start,meeting,end in zip(self.points, self.points[1:], self.points[2:]):
            yield Intersection(start,meeting,end)

    def angles(self):
        "Iterate all the three point angles"
        return [intersection.angle for intersection in self.intersections()]

    @property
    def length(self):
        "Measure the total length of the poly line"
        sum = 0.0
        for segment in self.segments():
            sum += segment.length
        return sum


    class MeasurementAlongPolyLine:
        def __init__(self, parent, index, remainder):
            self.parent = parent
            self.index = index
            self.remainder = remainder

        @property
        def segment(self):
            return self.parent.segments[self.index]

        @property
        def point(self):
            return self.segment.pointAlong(self.remainder);

    def measureAlong(self, w):
        sum = 0
        i = 0
        for segment in self.segments():
            if sum + segment.length < w:
                sum += segment.length
            else:
                return self.MeasurementAlongPolyLine(self, i, w - sum)
            i += 1
        # otherwise
        raise ValueError

    def pointAlong(self, w) -> vec2:
        "Find a point a certain distance along the polyline"
        return self.measureAlong(w).point

 

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
        measurement = self.measureAlong(w)
        point = measurement.point
        direction = measurement.segment.unitVector()
        return LineSegment(point, point + direction)

    def findCorners(self, threshholdAngle):
        "Find sharp corners in the line"
        # TODO

    def top(self) -> float:
        "y coordinate of the topmost point"
        return max([point.y for point in self.points])

    def bottom(self) -> float:
        "y coordinate of the bottom-most point"
        return min([point.y for point in self.points])

    def left(self) -> float:
        "x coordinate of the left-most point"
        return min([point.x for point in self.points])

    def right(self) -> float:
        "x coordinate of the right-most point"
        return max([point.x for point in self.points])

    def start(self) -> vec2:
        return self.points[0]

    def end(self) -> vec2:
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
