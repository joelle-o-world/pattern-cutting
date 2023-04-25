from src.geometry.Vector import Vector
from src.geometry.Group import Group
from .Shape import Shape
import numpy as np
from typing import List

from src.geometry.Mesh import Mesh


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
