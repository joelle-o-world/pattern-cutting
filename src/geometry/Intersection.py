import math

from src.geometry.angles import (
    anticlockwiseDifference,
    clockwiseDifference,
    normalizeAngle,
)
from src.geometry.LineSegment import LineSegment
from src.geometry.Vector import Vector


class Intersection:
    "Represents a point where two line segments meet"

    start: Vector
    meeting: Vector
    end: Vector

    def __init__(self, start, meeting, end):
        self.start = start
        self.meeting = meeting
        self.end = end

    @property
    def first(self):
        return LineSegment(self.start, self.meeting)

    @property
    def second(self):
        return LineSegment(self.meeting, self.end)

    @property
    def angle(self):
        return normalizeAngle(self.second.angle - self.first.angle)

    @property
    def clockwiseAngle(self):
        return clockwiseDifference(self.first.angle, self.second.angle + math.pi)

    @property
    def anticlockwiseAngle(self):
        return anticlockwiseDifference(self.first.angle, self.second.angle + math.pi)

    def bisect(self):
        vector = Vector(1, 0).withAngle(self.first.angle + self.clockwiseAngle / 2)
        return LineSegment(self.meeting, self.meeting + vector)

    def parallel(self, distance):
        "find a parallel intersection at a given distance"

        first = self.first.parallel(distance)
        second = self.second.parallel(distance)

        meeting = self.first.parallel(distance).extrapolatedIntersection(self.bisect())

        # meeting = first.extrapolatedIntersection(second)
        if meeting:
            return Intersection(start=first.start, meeting=meeting, end=second.end)
        else:
            raise Exception()
