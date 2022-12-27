from src.geometry.matrix_transformations import general_rotation, translate
from src.geometry.Shape import Shape
from src.geometry.Vector import Vector


class Shape3d:
    def __init__(self, points, label=None, style="line"):
        self.points = points
        self.label = label
        self.style = style

    def isometric(self):
        points = [
            Vector(x=point.x + point.z * 0.5, y=point.y + point.z * 0.5)
            for point in self.points
        ]
        return Shape(points, label=self.label, style=self.style)

    def transform(self, matrix):
        return Shape3d([point.transform(matrix) for point in self.points], label=self.label, style=self.style)

    def rotate(self, yaw=0.0, pitch=0.0, roll=0.0):
        matrix = general_rotation(yaw, pitch, roll)
        return self.transform(matrix)

    def translate(self, x=0.0, y=0.0, z=0.0):
        matrix = translate(x, y, z)
        return self.transform(matrix)

    def is_flat(self) -> bool:
        "If all the points are on the plane z=0 then the shape is 'flat'. This means it can be safely converted back to a 2d shape."
        for point in self.points:
            if point.z != 0:
                return False
        # Otherwise
        return True
