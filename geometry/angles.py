
import math

def normalizeAngle(angle: float):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle

def clockwiseDifference(a, b):
    print(a, b)
    while b > a + 2 * math.pi:
        b -= 2 * math.pi
    while b < a:
        b += 2 * math.pi
    print("->", b-a)
    return b - a


def anticlockwiseDifference(a, b):
    return clockwiseDifference(b,a) 
