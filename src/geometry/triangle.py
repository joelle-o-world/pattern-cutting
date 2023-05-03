import math


def triangle_area_2d(a, b, c):
    # Heron's formula
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))


def triangle_area_3d(a, b, c):
    ab = distance_3d(a, b)
    ac = distance_3d(a, c)
    bc = distance_3d(b, c)
    semiperimeter = (ac + ab + bc) / 2
    return math.sqrt(
        semiperimeter
        * (semiperimeter - bc)
        * (semiperimeter - ab)
        * (semiperimeter - ac)
    )


def triangle_point_collision(triangle, p) -> bool:
    a, b, c = triangle
    original_area = triangle_area_2d(a, b, c)
    area1 = triangle_area_2d(p, a, b)
    area2 = triangle_area_2d(p, a, c)
    area3 = triangle_area_2d(p, b, c)
    return area1 + area2 + area3 == original_area


def distance_3d(a, b):
    xa, ya, za = a
    xb, yb, zb = b
    return math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2 + (za - zb) ** 2)
