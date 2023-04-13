from src.geometry.Vector import Vector
from .Shape import Shape
import numpy as np


class Mesh:
    def __init__(self, vertices=[], faces=[], lines=[]):
        self.vertices = vertices
        self.lines = lines
        self.faces = faces

    def add_vertex(self, p):
        self.vertices.append(p)
        return len(self.vertices) - 1

    def add_face(self, a, b, c):
        if a != None and b != None and c != None:
            self.faces.append([a, b, c])


def triangulate(shape: Shape, cell_size=0.01):

    cell_width = cell_size
    cell_height = cell_size

    previous_row = [None for _ in np.arange(shape.left, shape.right, cell_width)]
    row = 0
    col = 0

    mesh = Mesh()
    for y in np.arange(shape.bottom, shape.top, cell_height):
        current_row = []
        for x in np.arange(shape.left, shape.right, cell_width):
            p = Vector(x, y)
            if shape.point_is_inside(p):
                current_row[col] = mesh.add_vertex(p)
                mesh.add_face(
                    current_row[col], current_row[col - 1], previous_row[col - 1]
                )
                mesh.add_face(
                    current_row[col], previous_row[col - 1], previous_row[col]
                )
            else:
                current_row[col] = None
            col += 1
        previous_row = current_row
        row += 1

    return mesh
