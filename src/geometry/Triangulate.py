from src.geometry.Vector import Vector
from src.geometry.Group import Group
from .Shape import Shape
import numpy as np
from typing import List


class Mesh:
    def __init__(self, vertices=[], faces=[], lines=[]):
        self.vertices = vertices
        self.lines = lines
        self.faces = faces

    def read_vertex_2d(self, index):
        return Vector(x=self.vertices[index][0], y=self.vertices[index][1])

    def add_vertex(self, x, y, z=0.0):
        self.vertices.append([x, y, z])
        return len(self.vertices) - 1

    def update_vertex(self, index, x: float, y: float, z=0.0):
        self.vertices[index] = [x, y, z]

    def add_face(self, a, b, c):
        if a != None and b != None and c != None:
            self.faces.append([a, b, c])

    def obj_str(self):
        str = ""
        for x, y, z in self.vertices:
            str += "v {} {} {}\n".format(x, y, z)
        for a, b, c in self.faces:
            str += "f {} {} {}\n".format(a, b, c)
        for a, b in self.lines:
            str += "l {} {}\n".format(a, b)
        return str

    def isometric(self):
        points = [
            Vector(x=point[0] + point[2] * 0.5, y=point[1] + point[2] * 0.5)
            for point in self.vertices
        ]
        faces = [
            Shape([points[face[0]], points[face[1]], points[face[2]]])
            for face in self.faces
        ]
        lines = [Shape([points[line[0]], points[line[1]]]) for line in self.lines]
        return Group(*faces, *lines)


def triangulate(shape: Shape, cell_size=10, snapping=True):

    cell_width = cell_size
    cell_height = cell_size

    previous_row = [None for _ in np.arange(shape.left, shape.right, cell_width)]
    row = 0

    mesh = Mesh()
    for y in np.arange(shape.bottom, shape.top, cell_height):
        current_row: List[int | None] = [
            None for _ in np.arange(shape.left, shape.right, cell_width)
        ]
        col = 0
        for x in np.arange(shape.left, shape.right, cell_width):
            p = Vector(x, y)
            if shape.point_is_inside(p):
                current_row[col] = mesh.add_vertex(x, y)
                if col > 0:
                    mesh.add_face(
                        current_row[col], current_row[col - 1], previous_row[col - 1]
                    )
                    mesh.add_face(
                        current_row[col], previous_row[col - 1], previous_row[col]
                    )
            else:
                current_row[col] = None
                left_neighbour_index = current_row[col - 1]
                if snapping and col > 0 and left_neighbour_index:
                    snapped_point = shape.closestPoint(
                        mesh.read_vertex_2d(left_neighbour_index)
                    )

                    mesh.update_vertex(
                        left_neighbour_index, snapped_point.x, snapped_point.y
                    )

            col += 1
        previous_row = current_row
        row += 1

    return mesh
