# This simple example draws a nice square

from geometry.Circle import Circle
from geometry.PolyLine import PolyLine
from geometry.vec2 import vec2
from render import render

square = PolyLine([vec2(0, 0), vec2(100, 0), vec2(100, 100), vec2(0, 100), vec2(0, 0)])
square.points[0].label = "first point"
sliced = square.slice(25, 175).translate(vec2(0, 200))

markers = square.evenlySpacedMeasurements()

circle = Circle(vec2(500, 500), 100).polyline(50)

drawing = render([
    square,
    square.points[0],
    *square.evenlySpacedMeasurements(),
    *square.corners(),
    sliced,
    *sliced.evenlySpacedMeasurements(),
    circle,
    *circle.corners(),
    *circle.evenlySpacedMeasurements()
])
drawing.saveSvg("Simple Example.svg")
print("Done!")
