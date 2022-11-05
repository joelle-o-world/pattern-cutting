import math
from typing import List

import drawSvg as draw
import numpy as np

from src.geometry.Intersection import Intersection
from src.geometry.LineSegment import LineSegment
from src.geometry.vec3 import vec3
from src.geometry.Vector import Vector, distance


class Shape:
    "As opposed to a monogamous line. This represents a shape made by many line segments joined end to end."
    points: List[Vector]
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
        self.points.append(Vector(p.x, p.y))

    def startAt(self, p):
        self.points = [p.copy()]

    def lineTo(self, p):
        self.append(p)

    def curveTo(self, p: Vector, curve=0):
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

    @property
    def numberOfPoints(self):
        return len(self.points)

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
    class MeasurementAlongShape:
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
                return self.MeasurementAlongShape(self, w, i, w - sum)
            i += 1
        # otherwise
        raise ValueError

    def pointAlong(self, w) -> Vector:
        "Find a point a certain distance along the polyline"
        return self.measureAlong(w).point

    def evenlySpacedMeasurements(self, step = 10):
        return [self.measureAlong(w) for w in np.arange(0, self.length, step)]

    def upsample(self):
        "Interpolate between the points to create a new poly line with greater resolution"
        # TODO

    def resample(self, interval):
        "Increase the resolution of the line, but no gaurantee for keeping the original points"
        points = []
        for l in np.arange(0, self.length, interval):
            points.append(self.at(l).point)
        if points[-1] != self.points[-1]:
            points.append(self.points[-1].copy())
        return Shape(points)

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


    def start(self) -> Vector:
        return self.points[0]

    def end(self) -> Vector:
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
        return Shape(
                points = self.points,
                label = self.label,
                style = style
            )

    def with_label(self, label: str):
        "Create a copy with a new label applied"
        return Shape(
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
        elif self.style == "polygon":
            return self.svg_polygon()
        elif self.style == "tape":
            return self.svg_tape()
        elif self.style == "ruler":
            return self.svg_ruler()
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

    def svg_line_only(self, close=False, fill="none", **kwargs):
        "Draw only the line as an svg <lines> element"
        return draw.Lines(*self.interleavedCoordinates(), close=close, fill=fill, stroke="black", **kwargs)

    def svg_dashed(self):
        g = draw.Group()
        line = self.svg_line_only(stroke_dasharray = "3")
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
            g.append(self.svg_centered_label())
        return g

    def center_of_mass(self):
        numberOfSamples = self.numberOfPoints * 2
        interval = self.length / numberOfSamples
        summed = Vector(0,0)
        n = 0.0
        for w in np.arange(0, self.length, interval):
            summed = summed + self.at(w).point
            n += 1 
        print(n)
        return summed / n


    def svg_centered_label(self):
        labelPosition = self.center_of_mass()
        return draw.Text(self.label, 12, labelPosition.x, labelPosition.y, stroke="none", fill="black", text_anchor="middle")

    def svg_polygon(self):
        group = draw.Group()
        group.append(self.svg_line_only( fill="#E6E6FA"))
        if self.label:
            group.append(self.svg_centered_label())
        return group

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
        arrow = draw.Marker(-1.0, -0.5, 0.9, 0.5, scale=8, orient='auto')
        arrow.append(draw.Lines(-1.0, -0.5, -1.0, 0.5, 0.0, 0, fill='black', stroke="none", close=True))
        line = self.svg_line_only(marker_end=arrow, **kwargs)
        g.append(line)
        if self.label:
            g.append(self.svg_parallel_label())
        return g

    def svg_dashed_arrow(self):
        return self.svg_arrow(stroke_dasharray="3")

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

    def svg_ruler(self, step=20):
        group = draw.Group()
        group.append(self.svg_line())
        for w in np.arange(0, self.length, step):
            m = self.at(w)
            marker = m.normal().withLength(-3)
            group.append(marker.svg())
            textPath = marker.withLength(100).translate(marker.vector.withLength(marker.length + 1))
            label = draw.Text("{:.0f}mm".format(w), 12, stroke='none', fill="#000000", path = textPath.svg())
            group.append(label)
        return group





    def __str__(self):
        points = ["{}".format(point) for point in self.points]
        return " -> ".join(points)

    def moveRight(self, amount):
        return self.translate(Vector(amount,0))

    def translate(self, t):
        return Shape([point + t for point in self.points], label=self.label, style=self.style)

    def move(self, x, y):
        return self.translate(Vector(x, y))

    def sliceAfter(self, start: int|float|Vector):
        startMeasurement = self.at(start)
        return Shape([
                startMeasurement.point,
                *self.points[startMeasurement.index + 1:]
            ])


    def slice(self, start: int|float | Vector, end: int|float | Vector | None= None):
        if end == None:
            return self.sliceAfter(start)
        startMeasurement = self.at(start)
        endMeasurement = self.at(end)
        if startMeasurement.index > endMeasurement.index:
            # Swap them
            swap = startMeasurement
            startMeasurement = endMeasurement
            endMeasurement = swap
        middlePoints = self.points[startMeasurement.index + 1 : endMeasurement.index + 1 ]
        return Shape([startMeasurement.point, *middlePoints, endMeasurement.point])

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

        return Shape([first, *inbetween,  last])


    def parallel(self, distance):
        # First point is drawn at a normal to the first segment
        first = self.firstSegment().parallel(distance).start

        # Same for the last point
        last = self.lastSegment().parallel(distance).end

        inbetween = [ intersection.parallel(distance).meeting for intersection in self.intersections()]
        return Shape([first, *inbetween, last])


    def closest(self, X: Vector) -> MeasurementAlongShape:
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
        return self.MeasurementAlongShape(self, w, winningIndex, remainder)

    def closestPoint(self, X) -> Vector:
        return self.closest(X).point


    def at(self, p: int| float | Vector) -> MeasurementAlongShape:
        "Find the point closest to the given coordinate, or a certain duration along the line"
        if isinstance(p, float) or isinstance(p, int):
            return self.measureAlong(p)
        else:
            return self.closest(p)

    def addDart(self, position: Vector | float | int, depth: float, width: float):
        at = self.at(position)
        lengthAlong = at.lengthAlong
        beforeDart = self.slice(0, lengthAlong - width/2)
        afterDart = self.slice(lengthAlong + width/2)
        dartPoint = at.normal().unitVector() * depth

        self.points = [*beforeDart.points, dartPoint, *afterDart.points]
        return self


    def interpolationCurves(self, curveSpeed=1):
        from src.geometry.bezier import BezierCurve
        q,r,s = self.points[:3]
        qrs = Intersection(q,r,s)
        qrDist = distance(q,r)
        guide1 = q + (r - q).withLength(qrDist / 2 * curveSpeed)
        guide2 = r + qrs.bisect().normal().withLength(qrDist / 2 * curveSpeed)
        yield BezierCurve(q, guide1, guide2, r)

        # Interpolate middle segments
        for i in range(3, len(self.points)):
            p,q,r,s = self.points[i-3:i+1]
            pqr = Intersection(p,q,r)
            qrs = Intersection(q,r,s)
            qrDist = distance(q,r)
            guide1 = q - pqr.bisect().normal().withLength(qrDist / 2 * curveSpeed)
            guide2 = r + qrs.bisect().normal().withLength(qrDist / 2 * curveSpeed)
            yield BezierCurve(q, guide1, guide2, r)

        p,q,r = self.points[-3:]
        pqr = Intersection(p,q,r)
        qrDist = distance(q,r)
        guide1 = q - pqr.bisect().normal().withLength(qrDist / 2 * curveSpeed)
        guide2 = r + (q - r).withLength(qrDist / 2 * curveSpeed)
        yield BezierCurve(q, guide1, guide2, r)


    def interpolate(self, curveSpeed=1, upres=20):
        points = []
        for curve in self.interpolationCurves(curveSpeed):
            points += curve.points(upres)[:-1]
        return Shape(points)

    def replace(self, replacementSection):
        before = self.slice(0, replacementSection.start())
        after = self.slice(replacementSection.end())
        return Shape(before.points + replacementSection.points + after.points)


    def to3D(self):
        from src.geometry.Shape3d import Shape3d
        points = [vec3(point.x, point.y, 0) for point in self.points]
        return Shape3d(points)
            




def arrow(*points, label=None):
    return Shape(points, style="arrow", label=label)

def dashed_arrow(*points, label=None):
    return Shape(points, style="dashed_arrow", label=label)

def dashed(*points, label=None):
    return Shape(points, style="dashed", label=label)
            



if __name__ == "__main__":
    square = Shape([Vector(1,1), Vector(1,100), Vector(100,100), Vector(100,1), Vector(1,1)])
    d = draw.Drawing(1000, 1000, origin='center',  stroke='black', fill='none')

    for angle in square.angles():
        print("Angle", math.degrees(angle))

    d.append(square.svg())
    d.saveSvg("example.svg")

    up = Vector(0, 1)
    print(up.angle)
    left = Vector(1,0)

