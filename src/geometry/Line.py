from src.geometry.Vector import Vector

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
            raise Exception("Lines are identical:", self,"and", other)
            
        elif self.gradient == other.gradient:
            # They are parallel 
            raise Exception("Lines are parallel and do not overlap:", self,"and", other)
        else:
            x = (other.intercept - self.intercept) / (self.gradient - other.gradient)
            y = self.y(x)
            return Vector(x, y)
