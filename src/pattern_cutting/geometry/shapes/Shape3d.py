from pattern_cutting.geometry.shapes.Shape import Shape
from pattern_cutting.geometry.vectors.Vector import Vector


class Shape3d:
    def __init__(self, points):
        self.points = points

    def isometric(self):
        points = [
            Vector(x=point.x + point.z * 0.5, y=point.y + point.z * 0.5)
            for point in self.points
        ]
        return Shape(points)
