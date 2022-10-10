from vec2 import vec2
from LineSegment import LineSegment
import math

class Intersection:
    "Represents a point where two line segments meet"

    start: vec2
    meeting: vec2
    end: vec2

    def __init__(self, start, meeting, end):
        self.start = start
        self.end = meeting
        self.end = end

    @property
    def first(self):
        return LineSegment(self.start, self.meeting)

    @property
    def second(self):
        return LineSegment(self.meeting, self.end)

    @property
    def angle(self):
        return self.first.angle + math.pi + self.second.angle

