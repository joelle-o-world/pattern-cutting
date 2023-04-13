from src.geometry.Vector import Vector
from .Shape import Shape
import numpy as np


class Mesh:
    def __init__(self, vertices=[], faces=[], lines=[]):
        self.vertices = vertices
        self.lines = lines
        self.faces = faces


def triangulate(shape: Shape, cell_size=0.01):

    cell_width = cell_size
    cell_height = cell_size

    previous_row = [None for _ in np.arange(shape.left, shape.right, cell_width)]
    row = 0
    col = 0

    vertices = []
    faces = []
    for y in np.arange(shape.bottom, shape.top, cell_height):
        current_row = []
        for x in np.arange(shape.left, shape.right, cell_width):
            p = Vector(x, y)
            if shape.point_is_inside(p):
                current_row[col] = len(vertices)
                vertices.append(p)
                # TODO: Use a conditional face adding function
                if current_row[col - 1] and previous_row[col - 1]:
                    faces.append([p, current_row[col - 1], previous_row[col - 1]])
                    pass
                if previous_row[col - 1] and previous_row[col]:
                    faces.append([p, previous_row[col - 1], previous_row[col]])
                    pass
            else:
                current_row[col] = None
            col += 1
        previous_row = current_row
        row += 1

    return Mesh(vertices=vertices, faces=faces)
