
import numpy as np
from math import cos,sin
    

def yaw(angle: float):
    return [
            [cos(angle), -sin(angle), 0,0],
            [sin(angle), cos(angle), 0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]

def pitch(angle: float):
    return [
            [cos(angle), 0, sin(angle),0],
            [ 0, 1, 0 ,0],
            [-sin(angle), 0, cos(angle),0],
            [0,0,0,1]
         ]

def roll(angle: float):
    return [
            [1, 0, 0,0],
            [0, cos(angle), -sin(angle),0],
            [0, sin(angle), cos(angle),0],
            [0,0,0,1]
         ]


def general_rotation(yaw_angle: float, pitch_angle: float, roll_angle: float):
    matrix = np.matmul(yaw(yaw_angle), pitch(pitch_angle))
    matrix = np.matmul(matrix, roll(roll_angle))
    return matrix

def translate(x=0.0, y=0.0, z=0.0):
    return [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [x,y,z,1]
        ]

def scale(x=1.0, y=1.0, z=1.0):
    return[
            [x,0,0,0],
            [0,y,0,0],
            [0,0,z,0],
            [0,0,0,1]
        ]

def shear(xy=0.0, xz=0.0, yx=0.0,yz=0.0, zx=0.0, zy=0.0):
    return [
            [1.0, yx, zx, 0.0],
            [xy, 1.0, zy, 0.0],
            [xz, yz, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]
