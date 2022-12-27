from src.geometry.matrix_transformations import general_rotation, translate
from src.geometry.Shape import Shape
from src.geometry.Vector import Vector


class Shape3d:
    def __init__(self, points):
        self.points = points

    def isometric(self):
        points = [
            Vector(x=point.x + point.z * 0.5, y=point.y + point.z * 0.5)
            for point in self.points
        ]
        return Shape(points)

    def transform(self, matrix):
        return Shape3d([point.transform(matrix) for point in self.points])

    def rotate(self, yaw=0.0, pitch=0.0, roll=0.0):
        matrix = general_rotation(yaw, pitch, roll)
        return self.transform(matrix)

    def translate(self, x=0.0, y=0.0, z=0.0):
        matrix = translate(x, y, z)
        return self.transform(matrix)
