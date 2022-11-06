import math


def normalize_angle(angle: float):
    """
    Normalize an angle in radians
    """
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def clockwise_difference(a, b):
    while b > a + 2 * math.pi:
        b -= 2 * math.pi
    while b < a:
        b += 2 * math.pi
    return b - a


def anticlockwise_difference(a, b):
    return clockwise_difference(b, a)
