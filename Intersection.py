from vec2 import vec2
from LineSegment import LineSegment

from angles import normalizeAngle

class Intersection:
    "Represents a point where two line segments meet"

    start: vec2
    meeting: vec2
    end: vec2

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


