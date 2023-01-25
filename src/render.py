import drawSvg as draw
import numpy as np
import string

from src.geometry.Rectangle import minimumBoundingRect
from src.geometry.Shape import Shape
from src.geometry.Vector import Vector

greek_aplhabet = [
    "α",
    "β",
    "γ",
    "δ",
    "ε",
    "ζ",
    "η",
    "θ",
    "ι",
    "κ",
    "λ",
    "μ",
    "ν",
    "ξ",
    "ο",
    "π",
    "ρ",
    "ς",
    "σ",
    "τ",
    "υ",
    "φ",
    "χ",
    "ψ",
    "ω",
]


def n2a(n, b=greek_aplhabet):
    d, m = divmod(n, len(b))
    return n2a(d - 1, b) + b[m] if d else b[m]


def render(*objects):
    "Quickly render any number of objects as SVG"

    actual_rect = minimumBoundingRect(objects)

    # Add a margin
    rect = actual_rect.enlarge(100)

    d = draw.Drawing(
        rect.width,
        rect.height,
        origin=(rect.left, rect.bottom),
        stroke="black",
        fill="none",
    )

    # Draw horizontal A4 lines
    gridColor = "#dddddd"
    for y in np.arange(rect.bottom, rect.top, 210):
        d.append(
            draw.Line(
                rect.left,
                y,
                rect.right,
                y,
                stroke=gridColor,
            )
        )

    # Draw vertical A4 lines
    for x in np.arange(rect.left, rect.right, 297):
        d.append(
            draw.Line(
                x,
                rect.bottom,
                x,
                rect.top,
                stroke=gridColor,
            )
        )

    # Draw A4 labels
    col = 0
    for x in np.arange(rect.left + 297 / 2, rect.right, 297):
        row = 0
        for y in np.arange(rect.bottom + 210 / 2, rect.top, 210):
            label = "{}{}".format(n2a(col), row)
            d.append(draw.Text(label, 10, x, y, stroke="none", fill=gridColor))

            row += 1
        col += 1

    gridSize = 50
    gridColor = "#ffcccc66"
    # Draw horizontal grid lines
    for y in np.arange(rect.bottom, rect.top, gridSize):
        d.append(
            draw.Line(rect.left, y, rect.right, y, stroke=gridColor, stroke_dasharray=5)
        )
        d.append(
            draw.Text(
                "{:.0f}mm".format(y - actual_rect.bottom),
                8,
                rect.left + 1,
                y + 2,
                stroke="none",
                fill=gridColor,
            )
        )

    # Draw vertical A4 lines
    for x in np.arange(rect.left, rect.right, gridSize):
        d.append(
            draw.Line(x, rect.bottom, x, rect.top, stroke=gridColor, stroke_dasharray=5)
        )
        d.append(
            draw.Text(
                "{:.0f}mm".format(x - actual_rect.left),
                8,
                x + 2,
                rect.bottom + 1,
                stroke="none",
                fill=gridColor,
            )
        )

    for object in objects:
        d.append(object.svg())

    return d
