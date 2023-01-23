from src.geometry.Group import Group
from src.seams import french_seam
from src.sizing.BodyMeasurements import BodyMeasurements, example_body_measurements
from src.geometry.Vector import Vector
from src.geometry.Shape import Shape
from src.finishings import rolled_hem
from src.units import inch


def tailored_skirt_block(
    body: BodyMeasurements = example_body_measurements, skirt_length=600.0
):
    p = [Vector(0, 0)] * 18

    p[1] = Vector(0, 0)

    # Square down and across from 1.
    # 1–2 half the hip measurement plus 1.5cm, square down; this line is the centre front line.
    p[2] = p[1].squareRight(body.hip / 2 + 15)

    # 1–3 skirt length, square across to 4 on the centre front line.
    p[3] = p[1].squareDown(skirt_length)
    p[4] = p[2].squareDown(skirt_length)

    # 1–5 waist to hip measurement, square across to 6 on the centre front line.
    p[5] = p[1].squareDown(body.waist_to_hip)
    p[6] = p[5].squareRight(p[2])

    # Back
    # 5–7 quarter the hip measurement plus 1.5cm ease, square down to 8 on the hemline.
    p[7] = p[5].squareRight(body.hip / 4 + 15)
    p[8] = p[7].squareDown(p[3])

    # 1–9 quarter waist measurement plus 4.25cm.
    p[9] = p[1].squareRight(body.waist / 4 + 42.5)

    # 9–10 1.25cm;
    # TODO: join 10 to points 1 and 7 with dotted lines.
    p[10] = p[9].squareUp(12.5)

    # Divide the line 1–10 into three parts, mark points 11 and 12.
    p[11] = p[1] + (p[10] - p[1]) / 3
    p[12] = p[11] + (p[10] - p[1]) / 3

    # Using the line 1–10, square down from points 11 and 12 with dotted lines.

    # TODO: Draw in the waistline with a slight curve;
    # TODO: draw in the side seam curving it outwards 0.5cm.

    # 2-15 quarter the waist measurement plus 2.25cm
    p[15] = p[2].squareLeft(body.waist / 4 + 22.5)

    # 15–16 1.25 cm, join 16 to points 2 and 7 with dotted lines
    p[16] = p[15].squareUp(12.5)

    # 16-17 is one third the distance 2–16; using the line 2–16, square down from 17 with a dotted line.
    p[17] = p[16] + (p[2] - p[16]) / 3

    for i in range(0, len(p)):
        p[i].label = "{}".format(i)

    # TODO: Draw in the waistline with a slight curve,
    # TODO: draw in the side seam curving outwards 0.5cm.

    back = Shape([p[i] for i in [1, 3, 8, 7, 10]], label="back").close()
    front = Shape([p[i] for i in [2, 16, 7, 8, 4]], label="front").close()

    # add a dart at p[11] 14 cm, 2cm wide
    back.addDart(p[11], 140, 20)

    #  dart at p[12] 12.5cm, 2cm wide
    back.addDart(p[12], 125, 20)

    #  Contsruct a dart at 17, length 10c; width 2cm
    front.addDart(p[17], 100, 20)

    g = Group(
        front=front,
        back=back,
    )
    g.label = "Tailored Skirt Block\nwaist={}\nhips={}\nwaist_to_hip={}\nskirt_length={}".format(
        body.waist, body.hip, body.waist_to_hip, skirt_length
    )
    for i in range(0, len(p)):
        g["p{}".format(i)] = p[i]

    return g

    # Special note for individual figures
    # If the waist is small in proportion to the hip size of the standard block, increase the width of the darts to 2.5cm. This will require you to draft:
    # 1–9 quarter waist plus 5.25cm.
    # 2–15 quarter waist plus 2.75cm.
    # This ensures a more even suppression around the waistline.


def complete_tailored_skirt_block(body=example_body_measurements, skirt_length=600):
    block = tailored_skirt_block(body, skirt_length)
    return block.add_objects(
        front_right=block["front"].flipped_horizontally(block["front"].right),
        back_right=block["back"].flipped_horizontally(block["back"].left),
    )


def tailored_skirt_pattern(
    body=example_body_measurements,
    skirt_length=600,
    bottom_hem_value=1.0 * inch,
    waist_hem_value=1 * inch,
    seam_allowance=1 * inch,
):
    block = complete_tailored_skirt_block(body=body, skirt_length=skirt_length)

    back_right = block.objects["back_right"]
    back = block.objects["back"]
    front = block.objects["front"]
    front_right = block.objects["front_right"]

    waist_line = Shape().line_through(
        back_right.sides()[3],
        back_right.sides()[6],
        back_right.sides()[9],
        back.sides()[9],
        back.sides()[6],
        back.sides()[3],
        front.sides()[3],
        front.sides()[0],
        front_right.sides()[0],
        front_right.sides()[3],
    )
    waist_hem = rolled_hem(waist_line, waist_hem_value)

    bottom_line = Shape().line_through(
        back_right.bottommost_side().reverse(),
        back.bottommost_side(),
        front.bottommost_side(),
        front_right.bottommost_side(),
    )

    bottom_hem = rolled_hem(bottom_line, -bottom_hem_value)

    seam = french_seam(
        back_right.leftmost_side(),
        front_right.rightmost_side().reverse(),
        seam_allowance,
    )
    allowances = Group(
        waist_hem=waist_hem,
        bottom_hem=bottom_hem,
        seam=seam,
    )

    return Group(block=block, allowances=allowances)
