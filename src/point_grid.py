import numpy as np
from .geometry.Vector import Vector
from .geometry.Shape import Shape


default_cell_width = 10.0


def point_grid(
    left: float, top: float, width: float, height: float, cell_width=default_cell_width
):
    cell_height = cell_width
    for x in np.arange(left, left + width, cell_width):
        for y in np.arange(top, top - height, -cell_height):
            yield Vector(x, y)


def point_grid_over_shape(shape: Shape, cell_width=default_cell_width, margin=0.0):
    return point_grid(
        left=shape.left - margin,
        top=shape.top + margin,
        width=shape.width + 2 * margin,
        height=shape.height + 2 * margin,
        cell_width=cell_width,
    )
