This is a python library for pattern cutting.

`Vector` class
--------------

A class for 2d cartesian coordinates. Its used for point coordinates and
also for 2d vectors


```python
from pattern_cutting.geometry.vectors.Vector import Vector

origin = Vector(0,0)
origin.label = "Origin"

```

You can use the render function to generate an SVG representation of the
geometry


```python
from pattern_cutting.render import render
render(origin)
```





![svg](readme_files/readme_3_0.svg)




Shape
-----

A `Shape` object is defined by multiple points which are joined by line
segemnts to create a complicated line or shape.


```python
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

    10.0






![svg](readme_files/readme_5_1.svg)




Using the `style` property, a polyline can be rendered as many different
kinds of shapes.


```python
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

    8.0
    8.0






![svg](readme_files/readme_7_1.svg)




You can draw measurement markers along a polyline:


```python
render(
  square,
  *square.evenlySpacedMeasurements()
)
```

    10.0






![svg](readme_files/readme_9_1.svg)




Or automatically detect corners:


```python
corners = square.corners()

render(
  square,
  *[corner.with_label("Here is a corner!") for corner in corners]
)
```

    10.0






![svg](readme_files/readme_11_1.svg)




You can slice out a certain portion of a line:


```python
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

    None 100
    None 30
    None 75.0
    10.0






![svg](readme_files/readme_13_1.svg)




The circle class can be used to generate regular polygons with so many
sides they look like a circle:


```python
from pattern_cutting.geometry.shapes.Circle import Circle

circle = Circle(Vector(0, 0), 100)
triangle = circle.polyline(3)
hexagon = circle.polyline(6)
almostCircle = circle.polyline(50)

from pattern_cutting.layout import sideBySide
render(*sideBySide(triangle, hexagon, almostCircle))
```

    None 150.00000000000006
    None 200.0
    None 200.0






![svg](readme_files/readme_15_1.svg)




We can put this together to get good approximations of measurements
along a curve:


```python
arc = circle.polyline(100).slice(0, 150)
render(
  arc,
  *arc.evenlySpacedMeasurements()
  )
```





![svg](readme_files/readme_17_0.svg)




Bezier Curves
-------------


```python
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





![svg](readme_files/readme_19_0.svg)




### Interpolating a `Shape` with Bizier Curves


```python
myshape = Shape([Vector(0,0), Vector(0, 200), Vector(200,250), Vector(250, 150), Vector(300 , 300)])

render(
  myshape.with_style("dashed"),
  myshape.interpolate(),
)
```





![svg](readme_files/readme_21_0.svg)




This makes a lot of points apear, so it might be a good idea to resample
the curve at lower resolution:


```python
interpolated = myshape.interpolate()
downsampled = interpolated.resample(25)
render(
  *topToBottom(
    interpolated.with_style("pointset"),
    downsampled.with_style("pointset").with_label("Re-sampled")
  )
)
```

    62.0






![svg](readme_files/readme_23_1.svg)




Demonstrating different curve speeds


```python
gen = [myshape]
for i in range(0, 20):
  next = myshape.interpolate((i+1) / 4)
  gen.append(next)

render(*gen)
```





![svg](readme_files/readme_25_0.svg)




Finding the closest point on a polyline
---------------------------------------

We can find the closest point on a polyline to any given coordinate:


```python
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





![svg](readme_files/readme_27_0.svg)




You can use closest points in other methods too, such as `slice`


```python
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

    None 92.95272905355262
    None 30
    None 32.867184771461226






![svg](readme_files/readme_29_1.svg)




Replacing a section of a shape
------------------------------

Here are two shapes


```python
a = Shape([Vector(-100, 200), Vector(200, -100)])
b = arc

render(a.with_label("a simple shape"), b.with_label("replacement"))
```





![svg](readme_files/readme_31_0.svg)




We can replace a region of one with the other


```python
render(a.replace(b))

```





![svg](readme_files/readme_33_0.svg)




Die Lemma dress block
---------------------

One of the main applications of this library is to create outfits for
East London drag queen [Die
Lemma](https://www.instagram.com/die.lemma/).

A dress block for Die was created and digitised into this library:


```python
from scripts.DieLemmaDressBlock import DieLemmaDressBlock

render(DieLemmaDressBlock)
```

    88.0






![svg](readme_files/readme_35_1.svg)




Drawing parallels to a complex polyline:


```python
render(
  DieLemmaDressBlock,
  DieLemmaDressBlock.parallel(50),
  *[dashed_arrow(P, Q) for P,Q in zip(DieLemmaDressBlock.points, DieLemmaDressBlock.parallel(50).points)],
  *DieLemmaDressBlock.points
)
```

    88.0






![svg](readme_files/readme_37_1.svg)




or drawing inside the shape instead of outside,


```python
render(
  DieLemmaDressBlock,
  DieLemmaDressBlock.parallel(-25),
  *[dashed_arrow(P, Q) for P,Q in zip(DieLemmaDressBlock.points, DieLemmaDressBlock.parallel(-25).points)],
  *DieLemmaDressBlock.points
)
```

    88.0






![svg](readme_files/readme_39_1.svg)




Winnifred Owen pattern blocks
-----------------------------

### Trouser block


```python
from scripts.TheClassicTailoredTrouserBlock import TheClassicTailoredTrouserBlock

render(TheClassicTailoredTrouserBlock())
```

    26.0






![svg](readme_files/readme_41_1.svg)




Working in 3D
-------------

Turn a 2d shape into 3d one (and back again to render it):


```python
square3d = square.to3D()

render(square3d.isometric())
```





![svg](readme_files/readme_43_0.svg)
