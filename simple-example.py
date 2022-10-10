# This simple example draws a nice square

from vec2 import vec2
from PolyLine import PolyLine
from render import render

square = PolyLine([vec2(0,0), vec2(100,0), vec2(100,100), vec2(0,100), vec2(0,0)])

drawing = render([square])
drawing.saveSvg("Simple Example.svg")
