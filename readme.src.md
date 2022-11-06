
This is a python library for pattern cutting.

## `Vector` class

A class for 2d cartesian coordinates. Its used for point coordinates and also for 2d vectors

```code
from pattern_cutting.geometry.vectors.Vector import Vector

origin = Vector(0,0)
origin.label = "Origin"

```

You can use the render function to generate an SVG representation of the geometry

```code
from pattern_cutting.render import render
render(origin)
```

## Shape

A `Shape` object is defined by multiple points which are joined by line segemnts to create a complicated line or shape.

```code
from pattern_cutting.geometry.shapes.Shape import Shape

square = Shape([
  Vector(0, 0),
  Vector(100, 0),
  Vector(100, 100),
  Vector(0, 100),
  Vector(0, 0)]
).with_label("a square").with_style("polygon")

render(square)
```

Using the `style` property, a polyline can be rendered as many different kinds of shapes.

```code
from pattern_cutting.layout import topToBottom

shape = Shape([Vector(0, 0), Vector(100, 50), Vector(200, -50), Vector(300, 0)])

render(
  *topToBottom(
    shape.with_style("line").with_label("line"),
    shape.with_style("dashed").with_label("dashed"),
    shape.with_style("arrow").with_label("arrow"),
    shape.with_style("dashed_arrow").with_label("dashed_arrow"),
    shape.with_style("pointset").with_label("pointset"),
    shape.with_style("polygon").with_label("polygon"),
    shape.with_style("tape").with_label("tape"),
    shape.with_style("ruler").with_label("ruler")
  )
)
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

render(
  square,
  *[corner.with_label("Here is a corner!") for corner in corners]
)
```

You can slice out a certain portion of a line:
```code
from pattern_cutting.layout import process
from pattern_cutting.geometry.Group import Group

P = square.at(25).point.with_label("P")
Q = square.at(175).point.with_label("Q")

render(
  *process(
    Group(
      square,
      P,
      Q,
    ),

    Group(
      square.slice(25, 175),
      P, Q
    )
  )
)
```

The circle class can be used to generate regular polygons with so many sides they look like a circle:

```code
from pattern_cutting.geometry.shapes.Circle import Circle

circle = Circle(Vector(0, 0), 100)
triangle = circle.polyline(3)
hexagon = circle.polyline(6)
almostCircle = circle.polyline(50)

from pattern_cutting.layout import sideBySide
render(*sideBySide(triangle, hexagon, almostCircle))
```

We can put this together to get good approximations of measurements along a curve:
```code
arc = circle.polyline(100).slice(0, 150)
render(
  arc,
  *arc.evenlySpacedMeasurements()
  )
```

## Bezier Curves

```code
from pattern_cutting.geometry.shapes.Shape import dashed
from pattern_cutting.geometry.bezier import BezierCurve
p0 = Vector(0,0).with_label("p0")
p1 = Vector(0, 50).with_label("p1")
p2 = Vector(50, 50).with_label("p2")
p3 = Vector(50, 100).with_label("p3")


mycurve = BezierCurve(p0, p1, p2, p3)

render(
  mycurve.demo()
  )
```

### Interpolating a `Shape` with Bizier Curves

```code
myshape = Shape([Vector(0,0), Vector(0, 200), Vector(200,250), Vector(250, 150), Vector(300 , 300)])

render(
  myshape.with_style("dashed"),
  myshape.interpolate(),
)
```

This makes a lot of points apear, so it might be a good idea to resample the curve at lower resolution:

```code
interpolated = myshape.interpolate()
downsampled = interpolated.resample(25)
render(
  *topToBottom(
    interpolated.with_style("pointset"),
    downsampled.with_style("pointset").with_label("Re-sampled")
  )
)
```

Demonstrating different curve speeds
```code
gen = [myshape]
for i in range(0, 20):
  next = myshape.interpolate((i+1) / 4)
  gen.append(next)

render(*gen)
```

## Finding the closest point on a polyline

We can find the closest point on a polyline to any given coordinate:
```code
from pattern_cutting.geometry.shapes.Shape import dashed_arrow
shape = arc
X = Vector(90, 100)
Y = shape.closestPoint(X)

render(
  shape,
  X.with_label("X"),
  Y.with_label("Y"),
  dashed_arrow(X, Y)
)
```

You can use closest points in other methods too, such as `slice`

```code
shape = arc
P = Vector(90, 100).with_label("P")
Q = Vector(100, 0).with_label("Q")
sliced = shape.slice(P, Q)
render(
  *process(
    Group(
      P,
      Q,
      dashed_arrow(P, shape.at(P).point),
      shape.with_label("Original"),
    ),
    Group(
      sliced.with_label("sliced"),
      *sliced.points, P, Q
    )
  )
  )
```


## Replacing a section of a shape

Here are two shapes
```code
a = Shape([Vector(-100, 200), Vector(200, -100)])
b = arc

render(a.with_label("a simple shape"), b.with_label("replacement"))
```

We can replace a region of one with the other

```code
render(a.replace(b))

```

## Die Lemma dress block

One of the main applications of this library is to create outfits for East London drag queen [Die Lemma](https://www.instagram.com/die.lemma/).

A dress block for Die was created and digitised into this library:

```code
from scripts.DieLemmaDressBlock import DieLemmaDressBlock

render(DieLemmaDressBlock)
```

Drawing parallels to a complex polyline:

```code
render(
  DieLemmaDressBlock,
  DieLemmaDressBlock.parallel(50),
  *[dashed_arrow(P, Q) for P,Q in zip(DieLemmaDressBlock.points, DieLemmaDressBlock.parallel(50).points)],
  *DieLemmaDressBlock.points
)
```

or drawing inside the shape instead of outside,

```code
render(
  DieLemmaDressBlock,
  DieLemmaDressBlock.parallel(-25),
  *[dashed_arrow(P, Q) for P,Q in zip(DieLemmaDressBlock.points, DieLemmaDressBlock.parallel(-25).points)],
  *DieLemmaDressBlock.points
)
```

## Winnifred Owen pattern blocks

### Trouser block

```code
from scripts.TheClassicTailoredTrouserBlock import TheClassicTailoredTrouserBlock

render(TheClassicTailoredTrouserBlock())
```

## Working in 3D

Turn a 2d shape into 3d one (and back again to render it):

```code
square3d = square.to3D()

render(square3d.isometric())
```
