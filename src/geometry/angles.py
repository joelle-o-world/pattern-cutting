import math


def normalizeAngle(angle: float):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def clockwiseDifference(a, b) -> float:
    while b > a + 2 * math.pi:
        b -= 2 * math.pi
    while b < a:
        b += 2 * math.pi
    return b - a


def anticlockwiseDifference(a, b):
    return clockwiseDifference(b, a)

def shortest_turn(a: float, b: float):
    clockwise = clockwiseDifference(a,b)
    anticlockwise= anticlockwiseDifference(a,b)
    if abs(clockwise) < abs(anticlockwise):
        return clockwise
    else:
        return anticlockwise

