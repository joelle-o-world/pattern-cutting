from layout import side_by_side
from src.geometry.Group import Group
from src.geometry.Vector import Vector
from src.geometry.Shape import Shape
import numpy as np
from src.geometry.Vector import Vector, polar

from src.geometry.angles import shortest_turn

def pointwise_tween(a: Shape, b: Shape, phase: float, resolution = 1.0) -> Shape:
    larger_length = max(a.length, b.length)

    shape = Shape()
    for w in np.arange(0, 1, resolution / larger_length):
        p = a.pointAlong(w * a.length)
        q = b.pointAlong(w * b.length)
        r = p + (q-p) * phase
        shape.line_to(r)
    return shape


def tween(a: Shape, b: Shape, phase: float, resolution = 1.0) -> Shape:
    larger_length = max(a.length, b.length)
    step = resolution / larger_length

    shape = Shape()
    shape.start_at(a.first_point * (1.0-phase) + b.first_point * phase)

    last_p = None
    last_q = None
    for w in np.arange(step, 1.0, step):
        p = a.pointAlong(w * a.length)
        q = b.pointAlong(w * b.length)
        if last_p:
            vP = p - last_p
            vQ = q - last_q
            turn = vP.angle + shortest_turn(vQ.angle, vP.angle) * phase
            length = vP.length * (1.0-phase) + phase * vQ.length
            shape.append(shape.last_point + polar(turn, length))
        last_p = p
        last_q = q


    return shape



def tween_demo(a: Shape, b:Shape):
    b = b.translate(Vector(750, 0))
    step = .05
    shapes = []
    shapes.append(a.with_label("A").with_style("arrow"))
    for phase in np.arange(step, 1.0, step):
        shapes.append(tween(a, b, phase).with_label("{:.0f}%".format(phase*100)).with_style("arrow"))

    shapes.append(b.with_label("B").with_style("arrow"))

    g = Group(*shapes)

    return g

