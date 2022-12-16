from src.geometry.Group import Group
from src.sizing.BodyMeasurements import BodyMeasurements, example_body_measurements
from src.geometry.Vector import Vector
from src.geometry.Shape import Shape

def tailored_skirt_block(body: BodyMeasurements = example_body_measurements, skirt_length=600.0):
    p = [Vector(0,0)] *  18

    p[1] = Vector(0,0)

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
    p[11] = p[1] + (p[10]-p[1]) / 3
    p[12] = p[11] + (p[10]-p[1]) / 3

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

    shape = Shape([p[i] for i in [1,3,4,2,16,7,10,1]])

    # shape.addDart(p[11], 140, 20)
    # TODO: add a dart at p[11] 14 cm, 2cm wide
    # TODO: dart at p[12] 12.5cm, 2cm wide
    # TODO: Contsruct a dart at 17, length 10c; width 2cm


    return Group(shape, *p)
    
    # Special note for individual figures
    # If the waist is small in proportion to the hip size of the standard block, increase the width of the darts to 2.5cm. This will require you to draft:
    # 1–9 quarter waist plus 5.25cm.
    # 2–15 quarter waist plus 2.75cm.
    # This ensures a more even suppression around the waistline.



