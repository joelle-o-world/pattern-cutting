from typing import List

import drawSvg as draw
import math
import numpy as np

from geometry.Intersection import Intersection
from geometry.LineSegment import LineSegment
from geometry.vec2 import vec2, distance, midpoint


class PolyLine:
    "As opposed to a monogamous line. This represents a shape made by many line segments joined end to end."
    points: List[vec2]
    style: str 
    label: str | None = None;



    # Construction
    def __init__(self, points = [], label=None, style="line"):
        self.label = label
        self.style = style
        self.points = [point.copy() for point in points]

    def firstPoint(self):
        return self.points[0]

    def lastPoint(self):
        return self.points[-1]

    def append(self, p):
        self.points.append(vec2(p.x, p.y))

    def startAt(self, p):
        self.points = [p.copy()]

    def lineTo(self, p):
        self.append(p)

    def curveTo(self, p: vec2, curve=0):
        # TODO: Create the actual curve
        self.append(p)


    def close(self):
        self.append(self.start())

    # Iteration
    def segments(self):
        "Iterate line segments"
        for start, end in zip(self.points, self.points[1:]):
            yield LineSegment(start, end)

    def segment(self, index):
        return LineSegment(
            start = self.points[index],
            end = self.points[index+1]
        )


    @property
    def numberOfSegments(self):
        return len(self.points) - 1

    def firstSegment(self):
        return self.segment(0)

    def lastSegment(self):
        return self.segment(self.numberOfSegments - 1)

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


    # TODO: Probably doesnt make sense for this to be a subclass any more
    # TODO: Define this class as a point a certain length along a line
    class MeasurementAlongPolyLine:
        def __init__(self, parent, lengthAlong: float, index, remainder):
            if remainder < 0:
                raise ValueError("Remainder should be greater than 0, got", remainder)
            self.parent = parent
            self.index = index
            self.remainder = remainder
            self.lengthAlong = lengthAlong

        @property
        def segment(self) ->  LineSegment:
            return self.parent.segment( self.index )

        @property
        def point(self):
            return self.segment.pointAlong(self.remainder);

        def normal(self):
            "Unit vector line segment perpendicular to the parent at this point"
            return self.segment.normalAlong(self.remainder)

        

        def svg(self):
            marker = self.normal().withLength(-3)
            textPath = marker.withLength(100).translate(marker.vector.withLength(marker.length + 1))
            label = draw.Text("{:.0f}mm".format(self.lengthAlong), 12, stroke='none', fill="#000000", path = textPath.svg())
            group = draw.Group()
            group.append(marker.svg())
            group.append(label)
            return group

        # TODO: Use a boundingRect() method instead
        @property
        def top(self): 
            return self.point.y
        @property
        def bottom(self): 
            return self.point.y
        @property
        def left(self): 
            return self.point.x
        @property
        def right(self): 
            return self.point.x

        @property
        def height(self):
            return self.top - self.bottom
        @property
        def width(self):
            return self.right - self.left

    def measureAlong(self, w: float | int):
        sum = 0
        i = 0
        for segment in self.segments():
            if sum + segment.length < w:
                sum += segment.length
            else:
                return self.MeasurementAlongPolyLine(self, w, i, w - sum)
            i += 1
        # otherwise
        raise ValueError

    def pointAlong(self, w) -> vec2:
        "Find a point a certain distance along the polyline"
        return self.measureAlong(w).point

    def evenlySpacedMeasurements(self, step = 10):
        return [self.measureAlong(w) for w in np.arange(0, self.length, step)]

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

    @property
    def top(self) -> float:
        "y coordinate of the topmost point"
        return max([point.y for point in self.points])

    @property
    def bottom(self) -> float:
        "y coordinate of the bottom-most point"
        return min([point.y for point in self.points])

    @property
    def left(self) -> float:
        "x coordinate of the left-most point"
        return min([point.x for point in self.points])

    @property
    def right(self) -> float:
        "x coordinate of the right-most point"
        return max([point.x for point in self.points])
    
    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return  self.top - self.bottom


    def start(self) -> vec2:
        return self.points[0]

    def end(self) -> vec2:
        return self.points[-1]


    # Exporting
    def interleavedCoordinates(self):
        for point in self.points:
            yield point.x
            yield point.y

    def labelText(self) -> str | None:
        return self.label

    def with_style(self, style: str):
        "Create a copy using a different style"
        return PolyLine(
                points = self.points,
                label = self.label,
                style = style
            )

    def with_label(self, label: str):
        "Create a copy with a new label applied"
        return PolyLine(
                points = self.points,
                label = label,
                style = self.style
            )

    def svg(self):
        "drawSvg object representation"
        if self.style == "line":
            return self.svg_line()
        elif self.style == "dashed":
            return self.svg_dashed()
        elif self.style == "pointset":
            return self.svg_pointset()
        elif self.style == "tape":
            return self.svg_tape()
        elif self.style == "arrow":
            return self.svg_arrow()
        elif self.style == "dashed_arrow":
            return self.svg_dashed_arrow()
        else:
            raise ValueError("Unable to render unexpected polyline style:", self.style)

    def svg_line(self):
        group = draw.Group()
        group.append(self.svg_line_only())
        if self.label:
            group.append(self.svg_parallel_label())
        return group

    def svg_line_only(self, **kwargs):
        "Draw only the line as an svg <lines> element"
        return draw.Lines(*self.interleavedCoordinates(), close=False, fill="none", stroke="black", **kwargs)

    def svg_dashed(self):
        g = draw.Group()
        line = self.svg_line_only(stroke_dasharray = "10")
        if self.label:
            g.append(self.svg_parallel_label())
        g.append(line)
        return g


    def svg_parallel_label(self):
        "Draw the label parallel to the line itself"
        return draw.Text(
                self.label, 12, 
                stroke = "none",
                fill = "#000000", 
                path = self.svg_line_only(), 
                startOffset = 10, 
                lineOffset = -1
            )

    def svg_pointset(self):
        g = draw.Group()
        for point in self.points:
            g.append(point.svg())
        if self.label:
            labelPosition = midpoint(*self.points)
            g.append(draw.Text(self.label, 12, labelPosition.x, labelPosition.y, stroke="none", fill="black", text_anchor="middle"))
        return g

    def svg_tape(self):
        g = draw.Group()
        g.append(self.svg_line_only())
        g.append(self.svg_start_notch())
        g.append(self.svg_end_notch())
        label = "{} ({:.1f}mm)".format(self.label, self.length) if self.label else "{:.1f}mm".format(self.length)
        g.append( draw.Text(
            label, 12, 
            path = self.svg_line_only(), 
            startOffset = 10, 
            lineOffset = -1,
            stroke="none",
            fill="black",
        ))
        return g

    def svg_arrow(self, **kwargs):
        g = draw.Group()
        arrow = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=8, orient='auto')
        arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', stroke="none", close=True))
        line = self.svg_line_only(marker_end=arrow, **kwargs)
        g.append(line)
        if self.label:
            g.append(self.svg_parallel_label())
        return g

    def svg_dashed_arrow(self):
        return self.svg_arrow(stroke_dasharray="10")





    def svg_perpendicular_notchthrough(self, at):
        position = self.at(at)
        normal = position.normal().unitVector() * 5
        P = position.point - normal
        Q = position.point + normal
        return draw.Line(*P.tuple, *Q.tuple, stroke="black")

    def svg_start_notch(self):
        return self.svg_perpendicular_notchthrough(0)
    def svg_end_notch(self):
        return self.svg_perpendicular_notchthrough(self.length)

        

            

    def __str__(self):
        points = ["{}".format(point) for point in self.points]
        return " -> ".join(points)

    def moveRight(self, amount):
        return self.translate(vec2(amount,0))

    def translate(self, t):
        return PolyLine([point + t for point in self.points], label=self.label, style=self.style)

    def move(self, x, y):
        return self.translate(vec2(x, y))

    def slice(self, start: int|float | vec2, end: int|float | vec2):
        startMeasurement = self.at(start)
        endMeasurement = self.at(end)
        if startMeasurement.index > endMeasurement.index:
            # Swap them
            swap = startMeasurement
            startMeasurement = endMeasurement
            endMeasurement = swap
        middlePoints = self.points[startMeasurement.index + 1 : endMeasurement.index ]
        return PolyLine([startMeasurement.point, *middlePoints, endMeasurement.point])

    def corners(self, threshholdAngle=math.radians(15)):
        "Find the corners that have an angle larger than the threshhold"
        return [intersection.meeting for intersection in self.intersections() if abs(intersection.angle) > threshholdAngle]


    def angleBisectionPathThing(self, distance):
        # First point is drawn at a normal to the first segment
        first = self.firstPoint() + self.firstSegment().normal().withLength(distance)

        # Same for the last point
        last = self.lastPoint() + self.lastSegment().normal().withLength(distance)

        # The inbetween points are drawn by bisecting the angle of the intersections 
        inbetween = [ intersection.bisect().withLength(distance).end for intersection in self.intersections() ]

        return PolyLine([first, *inbetween,  last])


    def parallel(self, distance):
        # First point is drawn at a normal to the first segment
        first = self.firstSegment().parallel(distance).start

        # Same for the last point
        last = self.lastSegment().parallel(distance).end

        inbetween = [ intersection.parallel(distance).meeting for intersection in self.intersections()]
        return PolyLine([first, *inbetween, last])


    def closest(self, X: vec2) -> MeasurementAlongPolyLine:
        # TODO: This needs to be simplified a lot
        Y = self.points[0]
        winningDistance = distance(X, Y)
        winningIndex = 0
        remainder = 0
        w = 0
        sum = 0
        i = 0
        for segment in self.segments():
            P = segment.closestPoint(X)
            dist = distance(P, X)
            if dist < winningDistance:
                Y = P
                winningDistance = dist
                winningIndex = i
                remainder = distance(segment.start, Y)
                w = sum + remainder
            i += 1
            sum += segment.length
        return self.MeasurementAlongPolyLine(self, w, winningIndex, remainder)

    def closestPoint(self, X) -> vec2:
        return self.closest(X).point


    def at(self, p: int| float | vec2) -> MeasurementAlongPolyLine:
        "Find the point closest to the given coordinate, or a certain duration along the line"
        if isinstance(p, float) or isinstance(p, int):
            return self.measureAlong(p)
        else:
            return self.closest(p)


            



if __name__ == "__main__":
    square = PolyLine([vec2(1,1), vec2(1,100), vec2(100,100), vec2(100,1), vec2(1,1)])
    d = draw.Drawing(1000, 1000, origin='center',  stroke='black', fill='none')

    for angle in square.angles():
        print("Angle", math.degrees(angle))

    d.append(square.svg())
    d.saveSvg("example.svg")

    up = vec2(0, 1)
    print(up.angle)
    left = vec2(1,0)

