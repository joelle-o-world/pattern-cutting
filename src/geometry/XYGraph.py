class XYGraph:
    intercept: float
    gradient: float

    def __init__(self, gradient=1.0, intercept=0.0):
        self.gradient = gradient
        self.intercept = intercept

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return XYGraph(gradient=self.gradient, intercept=self.intercept + other)
        elif isinstance(other, XYGraph):
            return XYGraph(
                intercept=self.intercept + other.intercept,
                gradient=self.gradient + other.gradient,
            )

    def __mul__(self, other: float | int):
        return XYGraph(gradient=self.gradient * other, intercept=self.intercept * other)

    def y(self, x: float):
        return x * self.gradient + self.intercept

    def x(self, y: float):
        return (y - self.intercept) / self.gradient
