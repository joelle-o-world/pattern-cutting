import drawSvg as draw

from src.geometry.Rectangle import minimumBoundingRect
from src.geometry.Shape import Shape
from src.geometry.Vector import Vector


def render(*objects):
    "Quickly render any number of objects as SVG"

    rect = minimumBoundingRect(objects)

    rect = rect.enlarge(50)
    bottomRuler = (
        Shape(style="faint_ruler")
        .startAt(Vector(rect.left, rect.bottom))
        .lineTo(Vector(rect.right, rect.bottom))
    )
    sideRuler = (
        Shape(style="faint_ruler")
        .startAt(Vector(rect.right, rect.bottom))
        .lineTo(Vector(rect.right, rect.top))
    )

    # Add a margin
    rect = rect.enlarge(100)

    d = draw.Drawing(
        rect.width,
        rect.height,
        origin=(rect.left, rect.bottom),
        stroke="black",
        fill="none",
    )

    for object in objects:
        d.append(object.svg())

    d.append(bottomRuler.svg())
    d.append(sideRuler.svg())

    return d
