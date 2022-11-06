import drawSvg as draw

from pattern_cutting.geometry.vectors.Vector import Vector, distance


class StraightLine:
    def __init__(self, gradient, intercept):
        self.gradient = gradient
        # NOTE: if gradient == float("inf") then intercept is on the x axis
        self.intercept = intercept

    @property
    def vertical(self):
        return self.gradient == float("inf")

    @property
    def horizontal(self):
        return self.gradient == 0

    def __str__(self):
        if self.vertical:
            return "x = {}".format(self.intercept)
        elif self.horizontal:
            return "y = {}".format(self.intercept)
        else:
            return "y = {}x + {}".format(self.gradient, self.intercept)

    def y(self, x):
        if self.vertical:
            raise Exception("Cannot find y position on vertical line")
        else:
            return self.intercept + self.gradient * x

    def intersectionPoint(self, other):
        if self == other:
            # They overlap
            raise Exception("Lines are identical:", self, "and", other)

        elif self.gradient == other.gradient:
            # They are parallel
            raise Exception(
                "Lines are parallel and do not overlap:", self, "and", other
            )
        else:
            x = (other.intercept - self.intercept) / (self.gradient - other.gradient)
            y = self.y(x)
            return Vector(x, y)


class LineSegment:
    "A line with a start and an end in 2d space"

    start: Vector
    end: Vector

    def __init__(self, start, end):
        if start == end:
            raise ValueError
        self.start = start
        self.end = end

    @property
    def vector(self):
        return self.end - self.start

    @vector.setter
    def vector(self, vector: Vector):
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

    def pointAlong(self, lengthAlong) -> Vector:
        if lengthAlong < 0 or lengthAlong > self.length:
            raise ValueError(
                "lengthAlong ({}) is out of bounds (0 to {})".format(
                    lengthAlong, self.length
                )
            )
        else:
            progress = lengthAlong / self.length
            return self.start * (1.0 - progress) + self.end * progress

    def normal(self) -> Vector:
        return self.vector.normal()

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
        return LineSegment(start=self.start + vec, end=self.end + vec)

    def gradient(self):
        if self.start.x == self.end.x:
            return float("inf")
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def vertical(self):
        return self.start.x == self.end.x

    def parallel(self, distance):
        return self.translate(self.normal().withLength(distance))

    def straightLine(self):
        if self.vertical():
            # Its vertical
            return StraightLine(gradient=float("inf"), intercept=self.start.x)
        else:
            gradient = self.gradient()
            intercept = self.start.y - self.start.x * gradient
            return StraightLine(gradient=gradient, intercept=intercept)

    def extrapolatedIntersection(self, other: "LineSegment"):
        def coeffs(line: LineSegment):
            A = line.start.y - line.end.y
            B = line.end.x - line.start.x
            C = line.start.x * line.end.y - line.end.x * line.start.y
            return A, B, -C

        L1 = coeffs(self)
        L2 = coeffs(other)
        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return Vector(x, y)
        else:
            return False

    def closestPoint(self, X: Vector) -> Vector:
        # TODO: there is so much that could be more efficient here!
        normal = self.normal()
        Y = self.extrapolatedIntersection(LineSegment(X, X + normal))
        if not Y:
            raise Exception("Something unexpected went wrong")
        XY = distance(X, Y)

        P = self.start
        Q = self.end
        x = (Y.x - P.x) / (Q.x - P.x)

        # y = (Y.y - P.y) / (Q.y - P.y)
        # if x != y:
        #     print("Something went wrong", x, y)

        if x < 0:
            return P
        elif x > 1:
            return Q
        else:
            return Y

        return Y

    # def extrapolatedIntersection(self, other: "LineSegment"):
    #     "Find the intersection between this line and another (using the infinite line, not the segment)"
    #     xdiff = (self.start.x - self.end.x, other.start.x - other.end.x)
    #     ydiff = (self.start.y - self.end.y, other.start.y - other.end.y)

    #     def det(a, b):
    #         return a[0] * b[1] - a[1] * b[0]

    #     div = det(xdiff, ydiff)
    #     if div == 0:
    #        raise Exception('lines do not intersect')

    #     d = (det(self.start.tuple, self.end.tuple), det(other.start.tuple, other.end.tuple))
    #     x = det(d, xdiff) / div
    #     y = det(d, ydiff) / div
    #     return vec2(x, y)
