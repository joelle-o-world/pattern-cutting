# This is a pattern Jane made when we were working on The Chicken Dress for Die Lemma (August 2022)
# I'm digitising it here based on measurements taken from the block

from geometry.vec2 import vec2
from geometry.PolyLine import PolyLine
from render import render

inch = 25.4

# These measurements (in inches) measure the width of the dress block from the top to bottom one inch apart
widthMeasurements = [ 10.4, 10.4, 10.3, 10.3, 10.2, 10.1, 9.8, 9.5, 9.1, 8.7,
                     8.3, 8.2, 8.3, 8.5, 8.7, 9.2, 9.7, 10.2, 10.7, 11.1, 11.5,
                     11.7, 11.7, 11.8, 11.8, 11.8, 11.9, 12.0, 12.0, 12.0,
                     12.0, 12.0, 12.0, 12.0, 12.1, 12.1, 12.2, 12.2, 12.2, 12.2
                     ]

overallHeightOfPatternPiece = 39.5 * inch

varyingSide = PolyLine()
y = overallHeightOfPatternPiece
for width in widthMeasurements:
    varyingSide.append(vec2(x=width * inch, y=y))
    y -= inch
varyingSide.append(vec2(varyingSide.end().x, 0))

shape = PolyLine([*varyingSide.points, vec2(0,0), vec2(0, varyingSide.top), varyingSide.start()])

if __name__ == "__main__":
    print(shape)
    render(shape, *shape.points).saveSvg("Die Lemma Dress Block.svg")
