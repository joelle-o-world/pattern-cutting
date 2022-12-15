import drawSvg as draw
import numpy as np

from src.geometry.Rectangle import minimumBoundingRect
from src.geometry.Shape import Shape
from src.geometry.Vector import Vector


def render(*objects):
    "Quickly render any number of objects as SVG"

    rect = minimumBoundingRect(objects)

    # Add a margin
    rect = rect.enlarge(100)

    d = draw.Drawing(
        rect.width,
        rect.height,
        origin=(rect.left, rect.bottom),
        stroke="black",
        fill="none",
    )

    # Draw horizontal lines
    gridColor = "#dddddd"
    gridSize = 50
    i = 0
    for y in np.arange(rect.bottom, rect.top, gridSize):
        dasharray = None if i % 5 == 0 else 5
        d.append(
            draw.Line(
                rect.left,
                y,
                rect.right,
                y,
                stroke=gridColor,
                stroke_dasharray=dasharray,
            )
        )
        i += 1
    i = 0
    for x in np.arange(rect.left, rect.right, gridSize):
        dasharray = None if i % 5 == 0 else 5
        d.append(
            draw.Line(
                x,
                rect.bottom,
                x,
                rect.top,
                stroke=gridColor,
                stroke_dasharray=dasharray,
            )
        )
        i += 1

    for object in objects:
        d.append(object.svg())

    return d
