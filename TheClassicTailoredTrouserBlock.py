from geometry.Vector import Vector, midpoint
from geometry.Shape import Shape
from BodyMeasurements import exampleBodyMeasurements, BodyMeasurements
from geometry.Group import Group

def TheClassicTailoredTrouserBlock(body: BodyMeasurements = exampleBodyMeasurements, bottomWidth: float = 220):
    "Create a trouser block according to Winnifred Owen instructions"
    p = [Vector(0,0)] * 16

    # Front
    # Square both ways from 0.
    p[0] = Vector(0,0)

    # 0–1 body rise; square across.
    p[1] = p[0].squareDown(body.bodyRise)

    # 0–2 waist to hip; square across.
    p[2] = p[0].squareDown(body.waistToHip)

    # 0–3 waist to floor measurement; square across.
    p[3] = p[0].squareDown(body.waistToFloor)

    # 1–4 half the measurement 1–3 minus 5cm; square across.
    p[4] = midpoint(p[1], p[3]).squareUp(50.0)

    # 1–5 one twelfth hip measurement plus 1.5cm; square up to 6 and 7.
    # quarter hip measurement plus 0.5cm.
    # one sixteenth hip measurement plus 0.5cm.
    p[5] = p[1].moveLeft(body.hip / 12 + 15)
    p[6] = p[5].squareUp(p[2])
    p[7] = p[5].squareUp(p[0])
    p[8] = p[6].squareRight(body.hip/4 + 5)
    p[9] = p[5].squareLeft(body.hip/16 + 5)

    # 7–10 -- 1cm; 
    p[10] = p[7] .squareRight(10.0)

    # TODO: join 10-6, join 6-9 with a curve touching a point:
    if  body.size <= 8:
        27.5
        # sizes 6–8 2.75cm fro5
    elif  body.size <= 14:
        30.0
        # sizes 10–14 3cm from5:
    elif body.size <= 20:
        32.5
        # sizes 16–20 3.25cm from5
    elif body.size <= 26:
        35.0
        # sizes 22–26 3.5cm from5
    else:
        raise Exception("Unhandled size {}".format(body.size))

    # 10–11 quarter waist plus 2.25cm.
    p[11] = p[10].squareRight(body.waist / 4 + 22.5)


    # 3–12 half trouser bottom width minus 0.5cm.
    p[12] = p[3].squareRight(bottomWidth / 2 - 5)

    # 4–13 the measurement 3–12 plus 1.3cm (sizes 16–20 1.5 cm; 22–24 1.7 cm).
    if body.size < 16:
        extraLittleBit = 1.3
    elif body.size <= 20:
        extraLittleBit = 1.5
    elif body.size <= 24:
        extraLittleBit = 1.7
    else:
        raise Exception("Unhandled size {}".format(body.size))
    p[13] = p[4].squareRight(
            (p[12]-p[3]).length + extraLittleBit
            )

    # TODO: Draw in side seam through points 11, 8, 13, 12; curve hipline outwards 0.5cm.

    # 3–14 half trouser bottom width minus 0.5cm.
    p[14] = p[3].squareLeft(bottomWidth/2 - 5)

    # 4–15 the measurement 4–13.
    p[15] = p[4].squareLeft((p[13]-p[4]).length)

    # TODO: Draw inside leg seam 9, 15, 14; curve 9–15 inwards 0.75 cm.

    for i in range(0, len(p)):
        p[i].label = "{}".format(i)



    shape = Shape([]).with_style("polygon")
    shape.startAt(p[9])
    # TODO: Curve inwards
    shape.curveTo(p[15])

    shape.lineTo(p[14])

    # TODO: Curve outwards
    shape.curveTo(p[12])

    shape.lineTo(p[13])
    shape.lineTo(p[8])

    # TODO: curve outwards
    shape.curveTo(p[11])

    shape.lineTo(p[10])
    shape.lineTo(p[6])
    shape.curveTo(p[9])

    # TODO: Construct a dart on the line from 0; length 10cm, width 2cm.
    shape.addDart(p[0], 100, 20)

    shape.label = "Classic Tailored Trouser Block - Front"

    return Group(shape, *p)
