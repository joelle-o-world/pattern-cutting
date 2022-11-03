# This simple example draws a nice square

from TheClassicTailoredTrouserBlock import TheClassicTailoredTrouserBlock
from geometry.Circle import Circle
from geometry.Shape import Shape
from geometry.DistanceMarker import DistanceMarker
from geometry.vec2 import vec2
from render import render
from layout import layout
from geometry.Group import Group

square = Shape([vec2(0, 0), vec2(100, 0), vec2(100, 100), vec2(0, 100), vec2(0, 0)])
square.points[0].label = "first point"
sliced = square.slice(25, 175).translate(vec2(0, 200))

markers = square.evenlySpacedMeasurements()

circle = Circle(vec2(500, 500), 100).polyline(50)
circle.points[3].label = "Fourth point"

circle.label = "Its a ciiircle"

distanceMarker = DistanceMarker([vec2(150, 100), vec2(110, 200)])

trousers = TheClassicTailoredTrouserBlock()

drawing = render(
        *layout([
            Group(
                circle, 
                *circle.corners(), 
                *circle.evenlySpacedMeasurements(25)
                ),
            Group(
                sliced,
                *sliced.evenlySpacedMeasurements(),
                ),
            distanceMarker,
            ])
        )

drawing.saveSvg("Simple Example.svg")

print("Done!")
