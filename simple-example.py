# This simple example draws a nice square

from vec2 import vec2
from PolyLine import PolyLine
from render import render

square = PolyLine([vec2(0,0), vec2(100,0), vec2(100,100), vec2(0,100), vec2(0,0)])
sliced = square.slice(25, 175).translate(vec2(0, 200))


markers = square.evenlySpacedMeasurements()

print([marker.svg() for marker in markers])

drawing = render([square, *markers, sliced, *sliced.evenlySpacedMeasurements()])
drawing.saveSvg("Simple Example.svg")
print("Done!")
