from src.geometry.Vector import Vector
from src.sizing.BodyMeasurements import BodyMeasurements
from src.geometry.Shape import Shape
from src.geometry.Group import Group
from src.units import inch


def denim_bandicoot_glove(body: BodyMeasurements, glove_length=12 * inch):

    palm = body.palm

    knuckles_x = 0

    wrap_around_knuckles = (
        Shape()
        .start_at(Vector(0, 0))
        .line_to(Vector(0, palm))
        .with_style("tape")
        .with_label("Wrap around knuckles")
    )

    knuckles_to_wrist = knuckles_x - body.knuckles_to_wrist
    wrist_x = knuckles_to_wrist
    elbow_x = wrist_x - body.wrist_to_elbow

    return Group(
        wrap_around_knuckles=wrap_around_knuckles,
        wrap_around_wrist=Shape(
            [Vector(wrist_x, 0), Vector(wrist_x, body.wrist)],
            label="Wrap around wrist",
            style="tape",
        ),
        wrap_around_elbow=Shape([Vector(elbow_x, body.elbow_circumference)]),
    )
