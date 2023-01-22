# This is a pattern Jane made when we were working on The Chicken Dress for Die Lemma (August 2022)
# I'm digitising it here based on measurements taken from the block

from src.render import render
from src.geometry.Shape import Shape
from src.geometry.Vector import Vector

inch = 25.4

# These measurements (in inches) measure the width of the dress block from the top to bottom one inch apart
widthMeasurements = [
    10.4,
    10.4,
    10.3,
    10.3,
    10.2,
    10.1,
    9.8,
    9.5,
    9.1,
    8.7,
    8.3,
    8.2,
    8.3,
    8.5,
    8.7,
    9.2,
    9.7,
    10.2,
    10.7,
    11.1,
    11.5,
    11.7,
    11.7,
    11.8,
    11.8,
    11.8,
    11.9,
    12.0,
    12.0,
    12.0,
    12.0,
    12.0,
    12.0,
    12.0,
    12.1,
    12.1,
    12.2,
    12.2,
    12.2,
    12.2,
]

overallHeightOfPatternPiece = 39.5 * inch

varyingSide = Shape()
y = overallHeightOfPatternPiece
for width in widthMeasurements:
    varyingSide.append(Vector(x=width * inch, y=y))
    y -= inch
varyingSide.append(Vector(varyingSide.end().x, 0))

DieLemmaDressBlock = Shape(
    [
        *varyingSide.points,
        Vector(0, 0),
        Vector(0, varyingSide.top),
        varyingSide.start(),
    ],
    style="polygon",
    label="Die Lemma Dress Block",
)

if __name__ == "__main__":
    print(DieLemmaDressBlock)
    render(DieLemmaDressBlock, *DieLemmaDressBlock.points).saveSvg(
        "Die Lemma Dress Block.svg"
    )
