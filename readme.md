# Pattern cutting

This is a python library for pattern cutting.


## `vec2` class

A class for 2d cartesian coordinates. Its used for point coordinates and also for 2d vectors

```code
from geometry.vec2 import vec2

origin = vec2(0,0)
origin.label = "Origin"

```

You can use the render function to generate an SVG representation of the geometry

```code
from render import render
render(origin)
```

## PolyLine

A `PolyLine` object is defined by multiple points which are joined by line segemnts to create a complicated line or shape.

```code
from geometry.PolyLine import PolyLine

square = PolyLine([vec2(0, 0), vec2(100, 0), vec2(100, 100), vec2(0, 100), vec2(0, 0)])

render(square)
```

You can draw measurement markers along a polyline:

```code
render(
  square, 
  *square.evenlySpacedMeasurements()
)
```

Or automatically detect corners:
```code
corners = square.corners()
for corner in corners:
  corner.label = "Here is a corner!"

render(
  square,
  *corners
)
```

You can slice out a certain portion of a line:
```code

render(
  square.slice(25, 175)
)
```

The circle class can be used to generate regular polygons with so many sides they look like a circle:

```code
from geometry.Circle import Circle

circle = Circle(vec2(0, 0), 100)
triangle = circle.polyline(3)
hexagon = circle.polyline(6)
almostCircle = circle.polyline(50)

from layout import layout
render(*layout([triangle, hexagon, almostCircle]))
```

We can put this together to get good approximations of measurements along a curve:
```code
arc = circle.polyline(100).slice(0, 150)
render(
  arc,
  *arc.evenlySpacedMeasurements()
  )
```


## Die Lemma dress block

One of the main applications of this library is to create outfits for east london drag queen [Die Lemma](https://www.instagram.com/die.lemma/).

A dress block for Die was created and digitised into this library:

```code
from DieLemmaDressBlock import DieLemmaDressBlock

render(DieLemmaDressBlock)
```

Drawing parallels to a complex polyline:

```code
render(
  DieLemmaDressBlock,
  DieLemmaDressBlock.parallel(50)
)
```

or drawing inside the shape instead of outside,

```code
render(
  DieLemmaDressBlock,
  DieLemmaDressBlock.parallel(-25)
)
```

## Winnifred Owen pattern blocks

### Trouser block

```code
from TheClassicTailoredTrouserBlock import TheClassicTailoredTrouserBlock

render(TheClassicTailoredTrouserBlock())
```
