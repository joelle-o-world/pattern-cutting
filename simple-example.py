# This simple example draws a nice square

from vec2 import vec2
from PolyLine import PolyLine
from render import render
from Circle import Circle

square = PolyLine([vec2(0,0), vec2(100,0), vec2(100,100), vec2(0,100), vec2(0,0)])
sliced = square.slice(25, 175).translate(vec2(0, 200))


markers = square.evenlySpacedMeasurements()


circle = Circle(vec2(500, 500), 100).polyline(50)


drawing = render([
    square, 
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
