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

## Die Lemma dress block

One of the main applications of this library is to create outfits for east london drag queen [Die Lemma](https://www.instagram.com/die.lemma/).

A dress block for Die was created and digitised into this library:

```code
from DieLemmaDressBlock import DieLemmaDressBlock

render(DieLemmaDressBlock)
```
