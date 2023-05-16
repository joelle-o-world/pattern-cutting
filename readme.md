This is a python library for pattern cutting.

## `Vector` class

A class for 2d cartesian coordinates. Its used for point coordinates and
also for 2d vectors


```python
from src.geometry.Vector import Vector

origin = Vector(0,0)
origin.label = "Origin"

```

You can use the render function to generate an SVG representation of the
geometry


```python
from src.render import render
render(origin)
```




    
![svg](readme_files/readme_3_0.svg)
    



## Shape

A `Shape` object is defined by multiple points which are joined by line
segemnts to create a complicated line or shape.


```python
from src.geometry.Shape import Shape

square = Shape([
  Vector(0, 0),
  Vector(100, 0),
  Vector(100, 100),
  Vector(0, 100),
  Vector(0, 0)]
).with_label("a square").with_style("polygon")

render(square)
```




    
![svg](readme_files/readme_5_0.svg)
    



Using the `style` property, a polyline can be rendered as many different
kinds of shapes.


```python
from layout import topToBottom

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




    
![svg](readme_files/readme_7_0.svg)
    



You can draw measurement markers along a polyline:


```python
render(
  square,
  *square.evenlySpacedMeasurements()
)
```




    
![svg](readme_files/readme_9_0.svg)
    



Or automatically detect corners:


```python
corners = square.corners()

render(
  square,
  *[corner.with_label("Here is a corner!") for corner in corners]
)
```




    
![svg](readme_files/readme_11_0.svg)
    



You can slice out a certain portion of a line:


```python
from layout import process
from src.geometry.Group import Group

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




    
![svg](readme_files/readme_13_0.svg)
    



The circle class can be used to generate regular polygons with so many
sides they look like a circle:


```python
from src.geometry.Circle import Circle

circle = Circle(Vector(0, 0), 100)
triangle = circle.polyline(3)
hexagon = circle.polyline(6)
almostCircle = circle.polyline(50)

from layout import sideBySide
render(*sideBySide(triangle, hexagon, almostCircle))
```




    
![svg](readme_files/readme_15_0.svg)
    



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
    



## Bezier Curves


```python
from src.geometry.Shape import dashed
from src.geometry.bezier import BezierCurve
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
    



### Interpolating a `Shape` with Bezier Curves


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




    
![svg](readme_files/readme_23_0.svg)
    



Demonstrating different curve speeds


```python
gen = [myshape]
for i in range(0, 20):
  next = myshape.interpolate((i+1) / 4)
  gen.append(next)

render(*gen)
```




    
![svg](readme_files/readme_25_0.svg)
    



## Finding the closest point on a polyline

We can find the closest point on a polyline to any given coordinate:


```python
from src.geometry.Shape import dashed_arrow
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




    
![svg](readme_files/readme_29_0.svg)
    



## Replacing a section of a shape

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
    



## Tweening between shapes

Tweening lets you morph one shape smoothly into another:


```python
from src.geometry.tween import tween, tween_demo

a = Shape([Vector(-100, 200), Vector(200, -100)])
b = arc

render(tween_demo(a, b))
```




    
![svg](readme_files/readme_35_0.svg)
    



A circle becoming a square,


```python
render(tween_demo(square, circle.polyline(100)))
```




    
![svg](readme_files/readme_37_0.svg)
    



## Turtle/Spirograph curves


```python
import math
from src.spirograph import spiro
angle_over_length = lambda x : math.radians(x*.1)
spiral = spiro(angle_over_length, 10000)
render(spiral)
```




    
![svg](readme_files/readme_39_0.svg)
    



## Adding darts


```python
shape = Shape([Vector(0,0), Vector(100, 0)])
shape.addDart(Vector(50, 0), 50, 20)
render(shape)
```




    
![svg](readme_files/readme_41_0.svg)
    




```python
shape = Shape([Vector(0,0), Vector(0, 100)])
shape.addDart(Vector(0, 50), 50, 20)
render(shape)
```




    
![svg](readme_files/readme_42_0.svg)
    



## Collision detection

Collision detection is powered by the
[qwertyquerty/collision](https://github.com/qwertyquerty/collision/blob/master/examples/concaves.py)
library.


```python
from src.geometry.Shape import rectangle
example_shape = rectangle(0, 0, 100, 100)
example_points = [Vector(50, 50), Vector(150, 50)]

for p in example_points:
  if example_shape.point_is_inside(p):
    p.label = "Collision!"
  else:
    p.label = "No collision!"

render(example_shape, *example_points)
```




    
![svg](readme_files/readme_44_0.svg)
    



Lets try something a bit trickier:


```python
from aldrich.tailored_skirt_block import tailored_skirt_block
from src.point_grid import point_grid_over_shape

example_shape = tailored_skirt_block()["back"]

points = []
for point in point_grid_over_shape(example_shape, margin=17):
  if example_shape.point_is_inside(point):
    points.append(point)

render(example_shape.with_style("all_guides"), *points)
  
```




    
![svg](readme_files/readme_46_0.svg)
    



## Triangulation

Turning a polygon into triangles:


```python
render(example_shape.earclip_mesh())
```

    data:application/object;charset=us-ascii;base64,diAwLjAgMC4wIDAuMAp2IDAgLTYwMC4wIDAuMAp2IDI0MC4wIC02MDAuMCAwLjAKdiAyNDAuMCAtNjAwLjAgMC4wCnYgMjQwLjAgLTI2NSAwLjAKdiAyMjMuNzUgMTIuNSAwLjAKdiAyNDAuMCAtNjAwLjAgMC4wCnYgMjIzLjc1IDEyLjUgMC4wCnYgMTU5LjE1MTA5ODA5MzI2OTk1IDguODkxMTIyNzk4NTA2NzAyIDAuMAp2IDI0MC4wIC02MDAuMCAwLjAKdiAxNTkuMTUxMDk4MDkzMjY5OTUgOC44OTExMjI3OTg1MDY3MDIgMC4wCnYgMTU2LjEzOTAzNDk4MTMzMzY1IC0xMTYuNDcyMDU5NDk5MjA2NyAwLjAKdiAxNTYuMTM5MDM0OTgxMzMzNjUgLTExNi40NzIwNTk0OTkyMDY3IDAuMAp2IDEzOS4xODIyMzUyNDAwNjM1NiA3Ljc3NTU0Mzg2ODE1OTk3NiAwLjAKdiA4NC41Njc3NjQ3NTk5MzY1MSA0LjcyNDQ1NjEzMTg0MDAyOSAwLjAKdiAxNTYuMTM5MDM0OTgxMzMzNjUgLTExNi40NzIwNTk0OTkyMDY3IDAuMAp2IDg0LjU2Nzc2NDc1OTkzNjUxIDQuNzI0NDU2MTMxODQwMDI5IDAuMAp2IDgyLjM5MjM4NTg0NTc2MDMyIC0xMzUuNjE1MzczMzA1Nzc4MTggMC4wCnYgODIuMzkyMzg1ODQ1NzYwMzIgLTEzNS42MTUzNzMzMDU3NzgxOCAwLjAKdiA2NC41OTg5MDE5MDY3MzAxIDMuNjA4ODc3MjAxNDkzMzAxNyAwLjAKdiAyNDAuMCAtNjAwLjAgMC4wCnYgMTU2LjEzOTAzNDk4MTMzMzY1IC0xMTYuNDcyMDU5NDk5MjA2NyAwLjAKdiA4Mi4zOTIzODU4NDU3NjAzMiAtMTM1LjYxNTM3MzMwNTc3ODE4IDAuMAp2IDI0MC4wIC02MDAuMCAwLjAKdiA4Mi4zOTIzODU4NDU3NjAzMiAtMTM1LjYxNTM3MzMwNTc3ODE4IDAuMAp2IDgyLjM5MjM4NTg0NTc2MDMyIC0xMzUuNjE1MzczMzA1Nzc4MTggMC4wCmYgMSAyIDMKZiA0IDUgNgpmIDcgOCA5CmYgMTAgMTEgMTIKZiAxMyAxNCAxNQpmIDE2IDE3IDE4CmYgMTkgMjAgMQpmIDIxIDIyIDIzCmYgMSAyNCAyNQo=





    
![svg](readme_files/readme_48_1.svg)
    



Sewing up the darts:


```python
mesh = example_shape.earclip_mesh()
sides = example_shape.sides()
mesh.add_seam(sides[7], sides[8].reverse())
mesh.add_seam(sides[4], sides[5].reverse())
render(mesh)
```

    data:application/object;charset=us-ascii;base64,diAwLjAgMC4wIDAuMAp2IDAgLTYwMC4wIDAuMAp2IDI0MC4wIC02MDAuMCAwLjAKdiAyNDAuMCAtNjAwLjAgMC4wCnYgMjQwLjAgLTI2NSAwLjAKdiAyMjMuNzUgMTIuNSAwLjAKdiAyNDAuMCAtNjAwLjAgMC4wCnYgMjIzLjc1IDEyLjUgMC4wCnYgMTU5LjE1MTA5ODA5MzI2OTk1IDguODkxMTIyNzk4NTA2NzAyIDAuMAp2IDI0MC4wIC02MDAuMCAwLjAKdiAxNTkuMTUxMDk4MDkzMjY5OTUgOC44OTExMjI3OTg1MDY3MDIgMC4wCnYgMTU2LjEzOTAzNDk4MTMzMzY1IC0xMTYuNDcyMDU5NDk5MjA2NyAwLjAKdiAxNTYuMTM5MDM0OTgxMzMzNjUgLTExNi40NzIwNTk0OTkyMDY3IDAuMAp2IDEzOS4xODIyMzUyNDAwNjM1NiA3Ljc3NTU0Mzg2ODE1OTk3NiAwLjAKdiA4NC41Njc3NjQ3NTk5MzY1MSA0LjcyNDQ1NjEzMTg0MDAyOSAwLjAKdiAxNTYuMTM5MDM0OTgxMzMzNjUgLTExNi40NzIwNTk0OTkyMDY3IDAuMAp2IDg0LjU2Nzc2NDc1OTkzNjUxIDQuNzI0NDU2MTMxODQwMDI5IDAuMAp2IDgyLjM5MjM4NTg0NTc2MDMyIC0xMzUuNjE1MzczMzA1Nzc4MTggMC4wCnYgODIuMzkyMzg1ODQ1NzYwMzIgLTEzNS42MTUzNzMzMDU3NzgxOCAwLjAKdiA2NC41OTg5MDE5MDY3MzAxIDMuNjA4ODc3MjAxNDkzMzAxNyAwLjAKdiAyNDAuMCAtNjAwLjAgMC4wCnYgMTU2LjEzOTAzNDk4MTMzMzY1IC0xMTYuNDcyMDU5NDk5MjA2NyAwLjAKdiA4Mi4zOTIzODU4NDU3NjAzMiAtMTM1LjYxNTM3MzMwNTc3ODE4IDAuMAp2IDI0MC4wIC02MDAuMCAwLjAKdiA4Mi4zOTIzODU4NDU3NjAzMiAtMTM1LjYxNTM3MzMwNTc3ODE4IDAuMAp2IDgyLjM5MjM4NTg0NTc2MDMyIC0xMzUuNjE1MzczMzA1Nzc4MTggMC4wCnYgODQuNTY3NzY0NzU5OTM2NTEgNC43MjQ0NTYxMzE4NDAwMjkgMC4wCnYgNjQuNTk4OTAxOTA2NzMwMSAzLjYwODg3NzIwMTQ5MzMwMTcgMC4wCnYgODQuNDEyNzc1NDI5Njk1NTYgLTUuMjc0MzQyNzExMzk2NjY1IDAuMAp2IDY1Ljg2NjYzNTE0NjM5MzI2IC02LjMxMDQzOTkzMzkyNzUyMSAwLjAKdiA4NC4yNTc3ODYwOTk0NTQ1OSAtMTUuMjczMTQxNTU0NjMzMzU5IDAuMAp2IDY3LjEzNDM2ODM4NjA1NjQxIC0xNi4yMjk3NTcwNjkzNDgzNDUgMC4wCnYgODQuMTAyNzk2NzY5MjEzNjQgLTI1LjI3MTk0MDM5Nzg3MDA1IDAuMAp2IDY4LjQwMjEwMTYyNTcxOTU3IC0yNi4xNDkwNzQyMDQ3NjkxNjQgMC4wCnYgODMuOTQ3ODA3NDM4OTcyNjkgLTM1LjI3MDczOTI0MTEwNjc0NiAwLjAKdiA2OS42Njk4MzQ4NjUzODI3MSAtMzYuMDY4MzkxMzQwMTg5OTkgMC4wCnYgODMuNzkyODE4MTA4NzMxNzQgLTQ1LjI2OTUzODA4NDM0MzQ0IDAuMAp2IDcwLjkzNzU2ODEwNTA0NTg3IC00NS45ODc3MDg0NzU2MTA4MTYgMC4wCnYgODMuNjM3ODI4Nzc4NDkwNzcgLTU1LjI2ODMzNjkyNzU4MDEzIDAuMAp2IDcyLjIwNTMwMTM0NDcwOTAzIC01NS45MDcwMjU2MTEwMzE2MzUgMC4wCnYgODMuNDgyODM5NDQ4MjQ5ODIgLTY1LjI2NzEzNTc3MDgxNjgyIDAuMAp2IDczLjQ3MzAzNDU4NDM3MjE5IC02NS44MjYzNDI3NDY0NTI0NyAwLjAKdiA4My4zMjc4NTAxMTgwMDg4NSAtNzUuMjY1OTM0NjE0MDUzNTIgMC4wCnYgNzQuNzQwNzY3ODI0MDM1MzMgLTc1Ljc0NTY1OTg4MTg3MzI4IDAuMAp2IDgzLjE3Mjg2MDc4Nzc2NzkyIC04NS4yNjQ3MzM0NTcyOTAyIDAuMAp2IDc2LjAwODUwMTA2MzY5ODQ3IC04NS42NjQ5NzcwMTcyOTQxIDAuMAp2IDgzLjAxNzg3MTQ1NzUyNjk1IC05NS4yNjM1MzIzMDA1MjY5IDAuMAp2IDc3LjI3NjIzNDMwMzM2MTYzIC05NS41ODQyOTQxNTI3MTQ5MyAwLjAKdiA4Mi44NjI4ODIxMjcyODU5OSAtMTA1LjI2MjMzMTE0Mzc2MzYgMC4wCnYgNzguNTQzOTY3NTQzMDI0NzkgLTEwNS41MDM2MTEyODgxMzU3NiAwLjAKdiA4Mi43MDc4OTI3OTcwNDUwMyAtMTE1LjI2MTEyOTk4NzAwMDI5IDAuMAp2IDc5LjgxMTcwMDc4MjY4Nzk0IC0xMTUuNDIyOTI4NDIzNTU2NTcgMC4wCnYgODIuNTUyOTAzNDY2ODA0MDggLTEyNS4yNTk5Mjg4MzAyMzY5OSAwLjAKdiA4MS4wNzk0MzQwMjIzNTExIC0xMjUuMzQyMjQ1NTU4OTc3NCAwLjAKdiA4Mi4zOTc5MTQxMzY1NjMxMyAtMTM1LjI1ODcyNzY3MzQ3MzcgMC4wCnYgODIuMzQ3MTY3MjYyMDE0MjUgLTEzNS4yNjE1NjI2OTQzOTgyNCAwLjAKdiAxNTkuMTUxMDk4MDkzMjY5OTUgOC44OTExMjI3OTg1MDY3MDIgMC4wCnYgMTM5LjE4MjIzNTI0MDA2MzU2IDcuNzc1NTQzODY4MTU5OTc2IDAuMAp2IDE1OC45MTA5MDA0NTA4Nzg1IC0xLjEwNTk5MjAzOTkxNDkxMSAwLjAKdiAxNDAuNTM0NDU5MDA0NjM3NiAtMi4xMzI2MDg4ODA0ODcwMzEgMC4wCnYgMTU4LjY3MDcwMjgwODQ4NzA1IC0xMS4xMDMxMDY4NzgzMzY1MjIgMC4wCnYgMTQxLjg4NjY4Mjc2OTIxMTYzIC0xMi4wNDA3NjE2MjkxMzQwMzUgMC4wCnYgMTU4LjQzMDUwNTE2NjA5NTYgLTIxLjEwMDIyMTcxNjc1ODE0IDAuMAp2IDE0My4yMzg5MDY1MzM3ODU2NyAtMjEuOTQ4OTE0Mzc3NzgxMDQ0IDAuMAp2IDE1OC4xOTAzMDc1MjM3MDQxMiAtMzEuMDk3MzM2NTU1MTc5NzQ4IDAuMAp2IDE0NC41OTExMzAyOTgzNTk3IC0zMS44NTcwNjcxMjY0MjgwNSAwLjAKdiAxNTcuOTUwMTA5ODgxMzEyNyAtNDEuMDk0NDUxMzkzNjAxMzcgMC4wCnYgMTQ1Ljk0MzM1NDA2MjkzMzc0IC00MS43NjUyMTk4NzUwNzUwNTQgMC4wCnYgMTU3LjcwOTkxMjIzODkyMTI1IC01MS4wOTE1NjYyMzIwMjI5OCAwLjAKdiAxNDcuMjk1NTc3ODI3NTA3NzcgLTUxLjY3MzM3MjYyMzcyMjA3IDAuMAp2IDE1Ny40Njk3MTQ1OTY1Mjk4IC02MS4wODg2ODEwNzA0NDQ2IDAuMAp2IDE0OC42NDc4MDE1OTIwODE4IC02MS41ODE1MjUzNzIzNjkwNyAwLjAKdiAxNTcuMjI5NTE2OTU0MTM4MzIgLTcxLjA4NTc5NTkwODg2NjIgMC4wCnYgMTUwLjAwMDAyNTM1NjY1NTg0IC03MS40ODk2NzgxMjEwMTYwNyAwLjAKdiAxNTYuOTg5MzE5MzExNzQ2ODcgLTgxLjA4MjkxMDc0NzI4NzgzIDAuMAp2IDE1MS4zNTIyNDkxMjEyMjk4NyAtODEuMzk3ODMwODY5NjYzMSAwLjAKdiAxNTYuNzQ5MTIxNjY5MzU1NDIgLTkxLjA4MDAyNTU4NTcwOTQ0IDAuMAp2IDE1Mi43MDQ0NzI4ODU4MDM5IC05MS4zMDU5ODM2MTgzMTAwOCAwLjAKdiAxNTYuNTA4OTI0MDI2OTYzOTcgLTEwMS4wNzcxNDA0MjQxMzEwNCAwLjAKdiAxNTQuMDU2Njk2NjUwMzc3OTQgLTEwMS4yMTQxMzYzNjY5NTcxIDAuMAp2IDE1Ni4yNjg3MjYzODQ1NzI1MiAtMTExLjA3NDI1NTI2MjU1MjY3IDAuMAp2IDE1NS40MDg5MjA0MTQ5NTE5OCAtMTExLjEyMjI4OTExNTYwNDEgMC4wCmYgMSAyIDMKZiA0IDUgNgpmIDcgOCA5CmYgMjEgMjIgMjMKZiAxIDI0IDI1CmYgMjkgMjcgMTYKZiAzMiAyMCAxCmYgMzMgMjkgMTYKZiAzNiAzMiAxOQpmIDM2IDMyIDEKZiAzNyAzMyAxNgpmIDQ2IDM2IDEKZiA0OCAxOSAxCmYgNDggNDYgMQpmIDU1IDM3IDE2CmYgNTUgMTYgMTgKZiA1OSAxMCAxMQpmIDU5IDExIDEyCmYgNjAgMjcgMTQKZiA2MSA1OSAxMApmIDYyIDYwIDI3CmYgNjMgNjEgMTAKZiA2NCA2MiAyNwpmIDY3IDYzIDEwCmYgNjcgNjMgMTIKZiA2OCA2NCAyNwpmIDY5IDY3IDEwCmYgNzIgNjggMjcKZiA3NiA3MiAyNwpmIDc4IDc2IDI3CmYgNzkgNjkgMTAKZiA3OSA2OSAxMgpmIDgwIDc4IDI3CmYgODAgMjcgMTMKZiA4MSA3OSAxMApmIDgxIDEwIDEyCmwgMjcgMjgKbCAyOSAzMApsIDMxIDMyCmwgMzMgMzQKbCAzNSAzNgpsIDM3IDM4CmwgMzkgNDAKbCA0MSA0MgpsIDQzIDQ0CmwgNDUgNDYKbCA0NyA0OApsIDQ5IDUwCmwgNTEgNTIKbCA1MyA1NApsIDU1IDU2CmwgNTcgNTgKbCA1OSA2MApsIDYxIDYyCmwgNjMgNjQKbCA2NSA2NgpsIDY3IDY4CmwgNjkgNzAKbCA3MSA3MgpsIDczIDc0CmwgNzUgNzYKbCA3NyA3OApsIDc5IDgwCmwgODEgODIK





    
![svg](readme_files/readme_50_1.svg)
    



## Die Lemma dress block

One of the main applications of this library is to create outfits for
East London drag queen [Die
Lemma](https://www.instagram.com/die.lemma/).

A dress block for Die was created and digitised into this library:


```python
from DieLemmaDressBlock import DieLemmaDressBlock

render(DieLemmaDressBlock)
```




    
![svg](readme_files/readme_52_0.svg)
    



Drawing parallels to a complex polyline:


```python
render(
  DieLemmaDressBlock,
  DieLemmaDressBlock.parallel(50),
  *[dashed_arrow(P, Q) for P,Q in zip(DieLemmaDressBlock.points, DieLemmaDressBlock.parallel(50).points)],
  *DieLemmaDressBlock.points
)
```




    
![svg](readme_files/readme_54_0.svg)
    



or drawing inside the shape instead of outside,


```python
render(
  DieLemmaDressBlock,
  DieLemmaDressBlock.parallel(-25),
  *[dashed_arrow(P, Q) for P,Q in zip(DieLemmaDressBlock.points, DieLemmaDressBlock.parallel(-25).points)],
  *DieLemmaDressBlock.points
)
```




    
![svg](readme_files/readme_56_0.svg)
    



## Winnifred Aldrich pattern blocks

One application of this library is quickly producing pattern blocks from
Winnfred Aldrich’s book. To do that, we have to be able to use describe
body measurements:


```python
from src.sizing.BodyMeasurements import example_body_measurements
print(example_body_measurements)
```

    Size 24.74583333333333:
    	waist	= 725.0mm	(-297.4mm)
    	hips	= 900.0mm	(-338.6mm)
    	waist_to_hip	= 265.0mm	(+39.9mm)
    	body_rise	= 340.0mm	(+8.3mm)
    	bust	= 1182.4mm
    	low_waist	= 1122.4mm
    	back_width	= 417.2mm
    	chest	= 414.7mm
    	shoulder	= 140.1mm
    	neck_size	= 443.2mm
    	dart	= 108.2mm
    	top_arm	= 379.5mm
    	wrist	= 196.6mm
    	ankle	= 276.6mm
    	high_ankle	= 246.6mm
    	nape_to_waist	= 435.5mm
    	front_shoulder_to_waist	= 462.4mm
    	armscye_depth	= 240.2mm
    	waist_to_knee	= 616.9mm
    	waist_to_floor	= 1103.7mm
    	sleeve_length	= 608.4mm
    	sleeve_length_jersey	= 568.4mm
    	cuff_size_shirts	= 241.9mm
    	cuff_size_two_piece_sleeve	= 153.4mm
    	trouser_bottom_width	= 251.9mm
    	jeans_bottom_width	= 210.0mm


### Trouser block


```python
from TheClassicTailoredTrouserBlock import TheClassicTailoredTrouserBlock

render(TheClassicTailoredTrouserBlock())
```




    
![svg](readme_files/readme_60_0.svg)
    



### Skirt block


```python
from aldrich.tailored_skirt_block import tailored_skirt_block

render(tailored_skirt_block())
```




    
![svg](readme_files/readme_62_0.svg)
    



Here it is with the seam and hems marked,


```python
from aldrich.tailored_skirt_block import tailored_skirt_pattern

render(tailored_skirt_pattern())
```

    Warning: creating french seam on two lines with different length: 612.9753811041546 and 613.3124368403252





    
![svg](readme_files/readme_64_1.svg)
    



I’m planning a long flared skirt.


```python
render(tailored_skirt_pattern(skirt_length=940, flare=1.4))
```

    Warning: creating french seam on two lines with different length: 958.9489488731247 and 959.2860046092952
    Warning: creating french seam on two lines with different length: 958.9489488731247 and 959.2860046092952





    
![svg](readme_files/readme_66_1.svg)
    



## Working in 3D

Turn a 2d shape into 3d one (and back again to render it):


```python
import numpy as np
square3d = square.to_3D()

render(
  *[
    square3d.rotate(pitch=angle).isometric() for angle in np.arange(0, 6.28, 0.3)
    ]
)
```




    
![svg](readme_files/readme_68_0.svg)
    



Tweening radially,


```python
shape_1 = Shape([Vector(0,0), Vector(50, -100)])
shape_2 = Shape([Vector(0,0), Vector(50, -15), Vector(50, -200)])

render(*[
  tween(shape_1, shape_2, phase).to_3D().rotate(pitch=phase * 3.14).isometric() for phase in np.arange(0, 1, .05)
])
```




    
![svg](readme_files/readme_70_0.svg)
    



### The `Mesh` class

For cloth simulation, we need to create a triangular mesh:


```python
from src.geometry.Mesh import mesh_grid

render(mesh_grid(300, 300))

```

    data:application/object;charset=us-ascii;base64,diAwIDAgMC4wCnYgMjUgMCAwLjAKdiA1MCAwIDAuMAp2IDc1IDAgMC4wCnYgMTAwIDAgMC4wCnYgMTI1IDAgMC4wCnYgMTUwIDAgMC4wCnYgMTc1IDAgMC4wCnYgMjAwIDAgMC4wCnYgMjI1IDAgMC4wCnYgMjUwIDAgMC4wCnYgMjc1IDAgMC4wCnYgMCAyNSAwLjAKdiAyNSAyNSAwLjAKdiA1MCAyNSAwLjAKdiA3NSAyNSAwLjAKdiAxMDAgMjUgMC4wCnYgMTI1IDI1IDAuMAp2IDE1MCAyNSAwLjAKdiAxNzUgMjUgMC4wCnYgMjAwIDI1IDAuMAp2IDIyNSAyNSAwLjAKdiAyNTAgMjUgMC4wCnYgMjc1IDI1IDAuMAp2IDAgNTAgMC4wCnYgMjUgNTAgMC4wCnYgNTAgNTAgMC4wCnYgNzUgNTAgMC4wCnYgMTAwIDUwIDAuMAp2IDEyNSA1MCAwLjAKdiAxNTAgNTAgMC4wCnYgMTc1IDUwIDAuMAp2IDIwMCA1MCAwLjAKdiAyMjUgNTAgMC4wCnYgMjUwIDUwIDAuMAp2IDI3NSA1MCAwLjAKdiAwIDc1IDAuMAp2IDI1IDc1IDAuMAp2IDUwIDc1IDAuMAp2IDc1IDc1IDAuMAp2IDEwMCA3NSAwLjAKdiAxMjUgNzUgMC4wCnYgMTUwIDc1IDAuMAp2IDE3NSA3NSAwLjAKdiAyMDAgNzUgMC4wCnYgMjI1IDc1IDAuMAp2IDI1MCA3NSAwLjAKdiAyNzUgNzUgMC4wCnYgMCAxMDAgMC4wCnYgMjUgMTAwIDAuMAp2IDUwIDEwMCAwLjAKdiA3NSAxMDAgMC4wCnYgMTAwIDEwMCAwLjAKdiAxMjUgMTAwIDAuMAp2IDE1MCAxMDAgMC4wCnYgMTc1IDEwMCAwLjAKdiAyMDAgMTAwIDAuMAp2IDIyNSAxMDAgMC4wCnYgMjUwIDEwMCAwLjAKdiAyNzUgMTAwIDAuMAp2IDAgMTI1IDAuMAp2IDI1IDEyNSAwLjAKdiA1MCAxMjUgMC4wCnYgNzUgMTI1IDAuMAp2IDEwMCAxMjUgMC4wCnYgMTI1IDEyNSAwLjAKdiAxNTAgMTI1IDAuMAp2IDE3NSAxMjUgMC4wCnYgMjAwIDEyNSAwLjAKdiAyMjUgMTI1IDAuMAp2IDI1MCAxMjUgMC4wCnYgMjc1IDEyNSAwLjAKdiAwIDE1MCAwLjAKdiAyNSAxNTAgMC4wCnYgNTAgMTUwIDAuMAp2IDc1IDE1MCAwLjAKdiAxMDAgMTUwIDAuMAp2IDEyNSAxNTAgMC4wCnYgMTUwIDE1MCAwLjAKdiAxNzUgMTUwIDAuMAp2IDIwMCAxNTAgMC4wCnYgMjI1IDE1MCAwLjAKdiAyNTAgMTUwIDAuMAp2IDI3NSAxNTAgMC4wCnYgMCAxNzUgMC4wCnYgMjUgMTc1IDAuMAp2IDUwIDE3NSAwLjAKdiA3NSAxNzUgMC4wCnYgMTAwIDE3NSAwLjAKdiAxMjUgMTc1IDAuMAp2IDE1MCAxNzUgMC4wCnYgMTc1IDE3NSAwLjAKdiAyMDAgMTc1IDAuMAp2IDIyNSAxNzUgMC4wCnYgMjUwIDE3NSAwLjAKdiAyNzUgMTc1IDAuMAp2IDAgMjAwIDAuMAp2IDI1IDIwMCAwLjAKdiA1MCAyMDAgMC4wCnYgNzUgMjAwIDAuMAp2IDEwMCAyMDAgMC4wCnYgMTI1IDIwMCAwLjAKdiAxNTAgMjAwIDAuMAp2IDE3NSAyMDAgMC4wCnYgMjAwIDIwMCAwLjAKdiAyMjUgMjAwIDAuMAp2IDI1MCAyMDAgMC4wCnYgMjc1IDIwMCAwLjAKdiAwIDIyNSAwLjAKdiAyNSAyMjUgMC4wCnYgNTAgMjI1IDAuMAp2IDc1IDIyNSAwLjAKdiAxMDAgMjI1IDAuMAp2IDEyNSAyMjUgMC4wCnYgMTUwIDIyNSAwLjAKdiAxNzUgMjI1IDAuMAp2IDIwMCAyMjUgMC4wCnYgMjI1IDIyNSAwLjAKdiAyNTAgMjI1IDAuMAp2IDI3NSAyMjUgMC4wCnYgMCAyNTAgMC4wCnYgMjUgMjUwIDAuMAp2IDUwIDI1MCAwLjAKdiA3NSAyNTAgMC4wCnYgMTAwIDI1MCAwLjAKdiAxMjUgMjUwIDAuMAp2IDE1MCAyNTAgMC4wCnYgMTc1IDI1MCAwLjAKdiAyMDAgMjUwIDAuMAp2IDIyNSAyNTAgMC4wCnYgMjUwIDI1MCAwLjAKdiAyNzUgMjUwIDAuMAp2IDAgMjc1IDAuMAp2IDI1IDI3NSAwLjAKdiA1MCAyNzUgMC4wCnYgNzUgMjc1IDAuMAp2IDEwMCAyNzUgMC4wCnYgMTI1IDI3NSAwLjAKdiAxNTAgMjc1IDAuMAp2IDE3NSAyNzUgMC4wCnYgMjAwIDI3NSAwLjAKdiAyMjUgMjc1IDAuMAp2IDI1MCAyNzUgMC4wCnYgMjc1IDI3NSAwLjAKZiAxMyAxNCAxCmYgMTQgMTUgMgpmIDE1IDE2IDMKZiAxNiAxNyA0CmYgMTcgMTggNQpmIDE4IDE5IDYKZiAxOSAyMCA3CmYgMjAgMjEgOApmIDIxIDIyIDkKZiAyMiAyMyAxMApmIDIzIDI0IDExCmYgMTQgMiAxCmYgMTUgMyAyCmYgMTYgNCAzCmYgMTcgNSA0CmYgMTggNiA1CmYgMTkgNyA2CmYgMjAgOCA3CmYgMjEgOSA4CmYgMjIgMTAgOQpmIDIzIDExIDEwCmYgMjQgMTIgMTEKZiAyNSAyNiAxMwpmIDI2IDI3IDE0CmYgMjcgMjggMTUKZiAyOCAyOSAxNgpmIDI5IDMwIDE3CmYgMzAgMzEgMTgKZiAzMSAzMiAxOQpmIDMyIDMzIDIwCmYgMzMgMzQgMjEKZiAzNCAzNSAyMgpmIDM1IDM2IDIzCmYgMjYgMTQgMTMKZiAyNyAxNSAxNApmIDI4IDE2IDE1CmYgMjkgMTcgMTYKZiAzMCAxOCAxNwpmIDMxIDE5IDE4CmYgMzIgMjAgMTkKZiAzMyAyMSAyMApmIDM0IDIyIDIxCmYgMzUgMjMgMjIKZiAzNiAyNCAyMwpmIDM3IDM4IDI1CmYgMzggMzkgMjYKZiAzOSA0MCAyNwpmIDQwIDQxIDI4CmYgNDEgNDIgMjkKZiA0MiA0MyAzMApmIDQzIDQ0IDMxCmYgNDQgNDUgMzIKZiA0NSA0NiAzMwpmIDQ2IDQ3IDM0CmYgNDcgNDggMzUKZiAzOCAyNiAyNQpmIDM5IDI3IDI2CmYgNDAgMjggMjcKZiA0MSAyOSAyOApmIDQyIDMwIDI5CmYgNDMgMzEgMzAKZiA0NCAzMiAzMQpmIDQ1IDMzIDMyCmYgNDYgMzQgMzMKZiA0NyAzNSAzNApmIDQ4IDM2IDM1CmYgNDkgNTAgMzcKZiA1MCA1MSAzOApmIDUxIDUyIDM5CmYgNTIgNTMgNDAKZiA1MyA1NCA0MQpmIDU0IDU1IDQyCmYgNTUgNTYgNDMKZiA1NiA1NyA0NApmIDU3IDU4IDQ1CmYgNTggNTkgNDYKZiA1OSA2MCA0NwpmIDUwIDM4IDM3CmYgNTEgMzkgMzgKZiA1MiA0MCAzOQpmIDUzIDQxIDQwCmYgNTQgNDIgNDEKZiA1NSA0MyA0MgpmIDU2IDQ0IDQzCmYgNTcgNDUgNDQKZiA1OCA0NiA0NQpmIDU5IDQ3IDQ2CmYgNjAgNDggNDcKZiA2MSA2MiA0OQpmIDYyIDYzIDUwCmYgNjMgNjQgNTEKZiA2NCA2NSA1MgpmIDY1IDY2IDUzCmYgNjYgNjcgNTQKZiA2NyA2OCA1NQpmIDY4IDY5IDU2CmYgNjkgNzAgNTcKZiA3MCA3MSA1OApmIDcxIDcyIDU5CmYgNjIgNTAgNDkKZiA2MyA1MSA1MApmIDY0IDUyIDUxCmYgNjUgNTMgNTIKZiA2NiA1NCA1MwpmIDY3IDU1IDU0CmYgNjggNTYgNTUKZiA2OSA1NyA1NgpmIDcwIDU4IDU3CmYgNzEgNTkgNTgKZiA3MiA2MCA1OQpmIDczIDc0IDYxCmYgNzQgNzUgNjIKZiA3NSA3NiA2MwpmIDc2IDc3IDY0CmYgNzcgNzggNjUKZiA3OCA3OSA2NgpmIDc5IDgwIDY3CmYgODAgODEgNjgKZiA4MSA4MiA2OQpmIDgyIDgzIDcwCmYgODMgODQgNzEKZiA3NCA2MiA2MQpmIDc1IDYzIDYyCmYgNzYgNjQgNjMKZiA3NyA2NSA2NApmIDc4IDY2IDY1CmYgNzkgNjcgNjYKZiA4MCA2OCA2NwpmIDgxIDY5IDY4CmYgODIgNzAgNjkKZiA4MyA3MSA3MApmIDg0IDcyIDcxCmYgODUgODYgNzMKZiA4NiA4NyA3NApmIDg3IDg4IDc1CmYgODggODkgNzYKZiA4OSA5MCA3NwpmIDkwIDkxIDc4CmYgOTEgOTIgNzkKZiA5MiA5MyA4MApmIDkzIDk0IDgxCmYgOTQgOTUgODIKZiA5NSA5NiA4MwpmIDg2IDc0IDczCmYgODcgNzUgNzQKZiA4OCA3NiA3NQpmIDg5IDc3IDc2CmYgOTAgNzggNzcKZiA5MSA3OSA3OApmIDkyIDgwIDc5CmYgOTMgODEgODAKZiA5NCA4MiA4MQpmIDk1IDgzIDgyCmYgOTYgODQgODMKZiA5NyA5OCA4NQpmIDk4IDk5IDg2CmYgOTkgMTAwIDg3CmYgMTAwIDEwMSA4OApmIDEwMSAxMDIgODkKZiAxMDIgMTAzIDkwCmYgMTAzIDEwNCA5MQpmIDEwNCAxMDUgOTIKZiAxMDUgMTA2IDkzCmYgMTA2IDEwNyA5NApmIDEwNyAxMDggOTUKZiA5OCA4NiA4NQpmIDk5IDg3IDg2CmYgMTAwIDg4IDg3CmYgMTAxIDg5IDg4CmYgMTAyIDkwIDg5CmYgMTAzIDkxIDkwCmYgMTA0IDkyIDkxCmYgMTA1IDkzIDkyCmYgMTA2IDk0IDkzCmYgMTA3IDk1IDk0CmYgMTA4IDk2IDk1CmYgMTA5IDExMCA5NwpmIDExMCAxMTEgOTgKZiAxMTEgMTEyIDk5CmYgMTEyIDExMyAxMDAKZiAxMTMgMTE0IDEwMQpmIDExNCAxMTUgMTAyCmYgMTE1IDExNiAxMDMKZiAxMTYgMTE3IDEwNApmIDExNyAxMTggMTA1CmYgMTE4IDExOSAxMDYKZiAxMTkgMTIwIDEwNwpmIDExMCA5OCA5NwpmIDExMSA5OSA5OApmIDExMiAxMDAgOTkKZiAxMTMgMTAxIDEwMApmIDExNCAxMDIgMTAxCmYgMTE1IDEwMyAxMDIKZiAxMTYgMTA0IDEwMwpmIDExNyAxMDUgMTA0CmYgMTE4IDEwNiAxMDUKZiAxMTkgMTA3IDEwNgpmIDEyMCAxMDggMTA3CmYgMTIxIDEyMiAxMDkKZiAxMjIgMTIzIDExMApmIDEyMyAxMjQgMTExCmYgMTI0IDEyNSAxMTIKZiAxMjUgMTI2IDExMwpmIDEyNiAxMjcgMTE0CmYgMTI3IDEyOCAxMTUKZiAxMjggMTI5IDExNgpmIDEyOSAxMzAgMTE3CmYgMTMwIDEzMSAxMTgKZiAxMzEgMTMyIDExOQpmIDEyMiAxMTAgMTA5CmYgMTIzIDExMSAxMTAKZiAxMjQgMTEyIDExMQpmIDEyNSAxMTMgMTEyCmYgMTI2IDExNCAxMTMKZiAxMjcgMTE1IDExNApmIDEyOCAxMTYgMTE1CmYgMTI5IDExNyAxMTYKZiAxMzAgMTE4IDExNwpmIDEzMSAxMTkgMTE4CmYgMTMyIDEyMCAxMTkKZiAxMzMgMTM0IDEyMQpmIDEzNCAxMzUgMTIyCmYgMTM1IDEzNiAxMjMKZiAxMzYgMTM3IDEyNApmIDEzNyAxMzggMTI1CmYgMTM4IDEzOSAxMjYKZiAxMzkgMTQwIDEyNwpmIDE0MCAxNDEgMTI4CmYgMTQxIDE0MiAxMjkKZiAxNDIgMTQzIDEzMApmIDE0MyAxNDQgMTMxCmYgMTM0IDEyMiAxMjEKZiAxMzUgMTIzIDEyMgpmIDEzNiAxMjQgMTIzCmYgMTM3IDEyNSAxMjQKZiAxMzggMTI2IDEyNQpmIDEzOSAxMjcgMTI2CmYgMTQwIDEyOCAxMjcKZiAxNDEgMTI5IDEyOApmIDE0MiAxMzAgMTI5CmYgMTQzIDEzMSAxMzAKZiAxNDQgMTMyIDEzMQo=





    
![svg](readme_files/readme_72_1.svg)
    



Interupting the mesh with a new point:


```python
my_mesh = mesh_grid(300, 300)
my_mesh.interupt_point((105, 115))
render(my_mesh)
```

    data:application/object;charset=us-ascii;base64,diAwIDAgMC4wCnYgMjUgMCAwLjAKdiA1MCAwIDAuMAp2IDc1IDAgMC4wCnYgMTAwIDAgMC4wCnYgMTI1IDAgMC4wCnYgMTUwIDAgMC4wCnYgMTc1IDAgMC4wCnYgMjAwIDAgMC4wCnYgMjI1IDAgMC4wCnYgMjUwIDAgMC4wCnYgMjc1IDAgMC4wCnYgMCAyNSAwLjAKdiAyNSAyNSAwLjAKdiA1MCAyNSAwLjAKdiA3NSAyNSAwLjAKdiAxMDAgMjUgMC4wCnYgMTI1IDI1IDAuMAp2IDE1MCAyNSAwLjAKdiAxNzUgMjUgMC4wCnYgMjAwIDI1IDAuMAp2IDIyNSAyNSAwLjAKdiAyNTAgMjUgMC4wCnYgMjc1IDI1IDAuMAp2IDAgNTAgMC4wCnYgMjUgNTAgMC4wCnYgNTAgNTAgMC4wCnYgNzUgNTAgMC4wCnYgMTAwIDUwIDAuMAp2IDEyNSA1MCAwLjAKdiAxNTAgNTAgMC4wCnYgMTc1IDUwIDAuMAp2IDIwMCA1MCAwLjAKdiAyMjUgNTAgMC4wCnYgMjUwIDUwIDAuMAp2IDI3NSA1MCAwLjAKdiAwIDc1IDAuMAp2IDI1IDc1IDAuMAp2IDUwIDc1IDAuMAp2IDc1IDc1IDAuMAp2IDEwMCA3NSAwLjAKdiAxMjUgNzUgMC4wCnYgMTUwIDc1IDAuMAp2IDE3NSA3NSAwLjAKdiAyMDAgNzUgMC4wCnYgMjI1IDc1IDAuMAp2IDI1MCA3NSAwLjAKdiAyNzUgNzUgMC4wCnYgMCAxMDAgMC4wCnYgMjUgMTAwIDAuMAp2IDUwIDEwMCAwLjAKdiA3NSAxMDAgMC4wCnYgMTAwIDEwMCAwLjAKdiAxMjUgMTAwIDAuMAp2IDE1MCAxMDAgMC4wCnYgMTc1IDEwMCAwLjAKdiAyMDAgMTAwIDAuMAp2IDIyNSAxMDAgMC4wCnYgMjUwIDEwMCAwLjAKdiAyNzUgMTAwIDAuMAp2IDAgMTI1IDAuMAp2IDI1IDEyNSAwLjAKdiA1MCAxMjUgMC4wCnYgNzUgMTI1IDAuMAp2IDEwMCAxMjUgMC4wCnYgMTI1IDEyNSAwLjAKdiAxNTAgMTI1IDAuMAp2IDE3NSAxMjUgMC4wCnYgMjAwIDEyNSAwLjAKdiAyMjUgMTI1IDAuMAp2IDI1MCAxMjUgMC4wCnYgMjc1IDEyNSAwLjAKdiAwIDE1MCAwLjAKdiAyNSAxNTAgMC4wCnYgNTAgMTUwIDAuMAp2IDc1IDE1MCAwLjAKdiAxMDAgMTUwIDAuMAp2IDEyNSAxNTAgMC4wCnYgMTUwIDE1MCAwLjAKdiAxNzUgMTUwIDAuMAp2IDIwMCAxNTAgMC4wCnYgMjI1IDE1MCAwLjAKdiAyNTAgMTUwIDAuMAp2IDI3NSAxNTAgMC4wCnYgMCAxNzUgMC4wCnYgMjUgMTc1IDAuMAp2IDUwIDE3NSAwLjAKdiA3NSAxNzUgMC4wCnYgMTAwIDE3NSAwLjAKdiAxMjUgMTc1IDAuMAp2IDE1MCAxNzUgMC4wCnYgMTc1IDE3NSAwLjAKdiAyMDAgMTc1IDAuMAp2IDIyNSAxNzUgMC4wCnYgMjUwIDE3NSAwLjAKdiAyNzUgMTc1IDAuMAp2IDAgMjAwIDAuMAp2IDI1IDIwMCAwLjAKdiA1MCAyMDAgMC4wCnYgNzUgMjAwIDAuMAp2IDEwMCAyMDAgMC4wCnYgMTI1IDIwMCAwLjAKdiAxNTAgMjAwIDAuMAp2IDE3NSAyMDAgMC4wCnYgMjAwIDIwMCAwLjAKdiAyMjUgMjAwIDAuMAp2IDI1MCAyMDAgMC4wCnYgMjc1IDIwMCAwLjAKdiAwIDIyNSAwLjAKdiAyNSAyMjUgMC4wCnYgNTAgMjI1IDAuMAp2IDc1IDIyNSAwLjAKdiAxMDAgMjI1IDAuMAp2IDEyNSAyMjUgMC4wCnYgMTUwIDIyNSAwLjAKdiAxNzUgMjI1IDAuMAp2IDIwMCAyMjUgMC4wCnYgMjI1IDIyNSAwLjAKdiAyNTAgMjI1IDAuMAp2IDI3NSAyMjUgMC4wCnYgMCAyNTAgMC4wCnYgMjUgMjUwIDAuMAp2IDUwIDI1MCAwLjAKdiA3NSAyNTAgMC4wCnYgMTAwIDI1MCAwLjAKdiAxMjUgMjUwIDAuMAp2IDE1MCAyNTAgMC4wCnYgMTc1IDI1MCAwLjAKdiAyMDAgMjUwIDAuMAp2IDIyNSAyNTAgMC4wCnYgMjUwIDI1MCAwLjAKdiAyNzUgMjUwIDAuMAp2IDAgMjc1IDAuMAp2IDI1IDI3NSAwLjAKdiA1MCAyNzUgMC4wCnYgNzUgMjc1IDAuMAp2IDEwMCAyNzUgMC4wCnYgMTI1IDI3NSAwLjAKdiAxNTAgMjc1IDAuMAp2IDE3NSAyNzUgMC4wCnYgMjAwIDI3NSAwLjAKdiAyMjUgMjc1IDAuMAp2IDI1MCAyNzUgMC4wCnYgMjc1IDI3NSAwLjAKdiAxMDUgMTE1IDAuMApmIDEzIDE0IDEKZiAxNCAxNSAyCmYgMTUgMTYgMwpmIDE2IDE3IDQKZiAxNyAxOCA1CmYgMTggMTkgNgpmIDE5IDIwIDcKZiAyMCAyMSA4CmYgMjEgMjIgOQpmIDIyIDIzIDEwCmYgMjMgMjQgMTEKZiAxNCAyIDEKZiAxNSAzIDIKZiAxNiA0IDMKZiAxNyA1IDQKZiAxOCA2IDUKZiAxOSA3IDYKZiAyMCA4IDcKZiAyMSA5IDgKZiAyMiAxMCA5CmYgMjMgMTEgMTAKZiAyNCAxMiAxMQpmIDI1IDI2IDEzCmYgMjYgMjcgMTQKZiAyNyAyOCAxNQpmIDI4IDI5IDE2CmYgMjkgMzAgMTcKZiAzMCAzMSAxOApmIDMxIDMyIDE5CmYgMzIgMzMgMjAKZiAzMyAzNCAyMQpmIDM0IDM1IDIyCmYgMzUgMzYgMjMKZiAyNiAxNCAxMwpmIDI3IDE1IDE0CmYgMjggMTYgMTUKZiAyOSAxNyAxNgpmIDMwIDE4IDE3CmYgMzEgMTkgMTgKZiAzMiAyMCAxOQpmIDMzIDIxIDIwCmYgMzQgMjIgMjEKZiAzNSAyMyAyMgpmIDM2IDI0IDIzCmYgMzcgMzggMjUKZiAzOCAzOSAyNgpmIDM5IDQwIDI3CmYgNDAgNDEgMjgKZiA0MSA0MiAyOQpmIDQyIDQzIDMwCmYgNDMgNDQgMzEKZiA0NCA0NSAzMgpmIDQ1IDQ2IDMzCmYgNDYgNDcgMzQKZiA0NyA0OCAzNQpmIDM4IDI2IDI1CmYgMzkgMjcgMjYKZiA0MCAyOCAyNwpmIDQxIDI5IDI4CmYgNDIgMzAgMjkKZiA0MyAzMSAzMApmIDQ0IDMyIDMxCmYgNDUgMzMgMzIKZiA0NiAzNCAzMwpmIDQ3IDM1IDM0CmYgNDggMzYgMzUKZiA0OSA1MCAzNwpmIDUwIDUxIDM4CmYgNTEgNTIgMzkKZiA1MiA1MyA0MApmIDUzIDU0IDQxCmYgNTQgNTUgNDIKZiA1NSA1NiA0MwpmIDU2IDU3IDQ0CmYgNTcgNTggNDUKZiA1OCA1OSA0NgpmIDU5IDYwIDQ3CmYgNTAgMzggMzcKZiA1MSAzOSAzOApmIDUyIDQwIDM5CmYgNTMgNDEgNDAKZiA1NCA0MiA0MQpmIDU1IDQzIDQyCmYgNTYgNDQgNDMKZiA1NyA0NSA0NApmIDU4IDQ2IDQ1CmYgNTkgNDcgNDYKZiA2MCA0OCA0NwpmIDYxIDYyIDQ5CmYgNjIgNjMgNTAKZiA2MyA2NCA1MQpmIDY0IDY1IDUyCmYgNjYgNjcgNTQKZiA2NyA2OCA1NQpmIDY4IDY5IDU2CmYgNjkgNzAgNTcKZiA3MCA3MSA1OApmIDcxIDcyIDU5CmYgNjIgNTAgNDkKZiA2MyA1MSA1MApmIDY0IDUyIDUxCmYgNjUgNTMgNTIKZiA2NiA1NCA1MwpmIDY3IDU1IDU0CmYgNjggNTYgNTUKZiA2OSA1NyA1NgpmIDcwIDU4IDU3CmYgNzEgNTkgNTgKZiA3MiA2MCA1OQpmIDczIDc0IDYxCmYgNzQgNzUgNjIKZiA3NSA3NiA2MwpmIDc2IDc3IDY0CmYgNzcgNzggNjUKZiA3OCA3OSA2NgpmIDc5IDgwIDY3CmYgODAgODEgNjgKZiA4MSA4MiA2OQpmIDgyIDgzIDcwCmYgODMgODQgNzEKZiA3NCA2MiA2MQpmIDc1IDYzIDYyCmYgNzYgNjQgNjMKZiA3NyA2NSA2NApmIDc4IDY2IDY1CmYgNzkgNjcgNjYKZiA4MCA2OCA2NwpmIDgxIDY5IDY4CmYgODIgNzAgNjkKZiA4MyA3MSA3MApmIDg0IDcyIDcxCmYgODUgODYgNzMKZiA4NiA4NyA3NApmIDg3IDg4IDc1CmYgODggODkgNzYKZiA4OSA5MCA3NwpmIDkwIDkxIDc4CmYgOTEgOTIgNzkKZiA5MiA5MyA4MApmIDkzIDk0IDgxCmYgOTQgOTUgODIKZiA5NSA5NiA4MwpmIDg2IDc0IDczCmYgODcgNzUgNzQKZiA4OCA3NiA3NQpmIDg5IDc3IDc2CmYgOTAgNzggNzcKZiA5MSA3OSA3OApmIDkyIDgwIDc5CmYgOTMgODEgODAKZiA5NCA4MiA4MQpmIDk1IDgzIDgyCmYgOTYgODQgODMKZiA5NyA5OCA4NQpmIDk4IDk5IDg2CmYgOTkgMTAwIDg3CmYgMTAwIDEwMSA4OApmIDEwMSAxMDIgODkKZiAxMDIgMTAzIDkwCmYgMTAzIDEwNCA5MQpmIDEwNCAxMDUgOTIKZiAxMDUgMTA2IDkzCmYgMTA2IDEwNyA5NApmIDEwNyAxMDggOTUKZiA5OCA4NiA4NQpmIDk5IDg3IDg2CmYgMTAwIDg4IDg3CmYgMTAxIDg5IDg4CmYgMTAyIDkwIDg5CmYgMTAzIDkxIDkwCmYgMTA0IDkyIDkxCmYgMTA1IDkzIDkyCmYgMTA2IDk0IDkzCmYgMTA3IDk1IDk0CmYgMTA4IDk2IDk1CmYgMTA5IDExMCA5NwpmIDExMCAxMTEgOTgKZiAxMTEgMTEyIDk5CmYgMTEyIDExMyAxMDAKZiAxMTMgMTE0IDEwMQpmIDExNCAxMTUgMTAyCmYgMTE1IDExNiAxMDMKZiAxMTYgMTE3IDEwNApmIDExNyAxMTggMTA1CmYgMTE4IDExOSAxMDYKZiAxMTkgMTIwIDEwNwpmIDExMCA5OCA5NwpmIDExMSA5OSA5OApmIDExMiAxMDAgOTkKZiAxMTMgMTAxIDEwMApmIDExNCAxMDIgMTAxCmYgMTE1IDEwMyAxMDIKZiAxMTYgMTA0IDEwMwpmIDExNyAxMDUgMTA0CmYgMTE4IDEwNiAxMDUKZiAxMTkgMTA3IDEwNgpmIDEyMCAxMDggMTA3CmYgMTIxIDEyMiAxMDkKZiAxMjIgMTIzIDExMApmIDEyMyAxMjQgMTExCmYgMTI0IDEyNSAxMTIKZiAxMjUgMTI2IDExMwpmIDEyNiAxMjcgMTE0CmYgMTI3IDEyOCAxMTUKZiAxMjggMTI5IDExNgpmIDEyOSAxMzAgMTE3CmYgMTMwIDEzMSAxMTgKZiAxMzEgMTMyIDExOQpmIDEyMiAxMTAgMTA5CmYgMTIzIDExMSAxMTAKZiAxMjQgMTEyIDExMQpmIDEyNSAxMTMgMTEyCmYgMTI2IDExNCAxMTMKZiAxMjcgMTE1IDExNApmIDEyOCAxMTYgMTE1CmYgMTI5IDExNyAxMTYKZiAxMzAgMTE4IDExNwpmIDEzMSAxMTkgMTE4CmYgMTMyIDEyMCAxMTkKZiAxMzMgMTM0IDEyMQpmIDEzNCAxMzUgMTIyCmYgMTM1IDEzNiAxMjMKZiAxMzYgMTM3IDEyNApmIDEzNyAxMzggMTI1CmYgMTM4IDEzOSAxMjYKZiAxMzkgMTQwIDEyNwpmIDE0MCAxNDEgMTI4CmYgMTQxIDE0MiAxMjkKZiAxNDIgMTQzIDEzMApmIDE0MyAxNDQgMTMxCmYgMTM0IDEyMiAxMjEKZiAxMzUgMTIzIDEyMgpmIDEzNiAxMjQgMTIzCmYgMTM3IDEyNSAxMjQKZiAxMzggMTI2IDEyNQpmIDEzOSAxMjcgMTI2CmYgMTQwIDEyOCAxMjcKZiAxNDEgMTI5IDEyOApmIDE0MiAxMzAgMTI5CmYgMTQzIDEzMSAxMzAKZiAxNDQgMTMyIDEzMQpmIDE0NSA2NSA2NgpmIDE0NSA2NiA1MwpmIDE0NSA2NSA1Mwo=





    
![svg](readme_files/readme_74_1.svg)
    



I want to sew the sides of this together to make a tube.O


```python
tube = mesh_grid(300, 300)
left_side = Shape([Vector(0,0), Vector(0, 250)])
right_side = Shape([Vector(250,0), Vector(250, 250)])
tube.add_seam(left_side, right_side)
render (tube)
```

    data:application/object;charset=us-ascii;base64,diAwIDAgMC4wCnYgMjUgMCAwLjAKdiA1MCAwIDAuMAp2IDc1IDAgMC4wCnYgMTAwIDAgMC4wCnYgMTI1IDAgMC4wCnYgMTUwIDAgMC4wCnYgMTc1IDAgMC4wCnYgMjAwIDAgMC4wCnYgMjI1IDAgMC4wCnYgMjUwIDAgMC4wCnYgMjc1IDAgMC4wCnYgMCAyNSAwLjAKdiAyNSAyNSAwLjAKdiA1MCAyNSAwLjAKdiA3NSAyNSAwLjAKdiAxMDAgMjUgMC4wCnYgMTI1IDI1IDAuMAp2IDE1MCAyNSAwLjAKdiAxNzUgMjUgMC4wCnYgMjAwIDI1IDAuMAp2IDIyNSAyNSAwLjAKdiAyNTAgMjUgMC4wCnYgMjc1IDI1IDAuMAp2IDAgNTAgMC4wCnYgMjUgNTAgMC4wCnYgNTAgNTAgMC4wCnYgNzUgNTAgMC4wCnYgMTAwIDUwIDAuMAp2IDEyNSA1MCAwLjAKdiAxNTAgNTAgMC4wCnYgMTc1IDUwIDAuMAp2IDIwMCA1MCAwLjAKdiAyMjUgNTAgMC4wCnYgMjUwIDUwIDAuMAp2IDI3NSA1MCAwLjAKdiAwIDc1IDAuMAp2IDI1IDc1IDAuMAp2IDUwIDc1IDAuMAp2IDc1IDc1IDAuMAp2IDEwMCA3NSAwLjAKdiAxMjUgNzUgMC4wCnYgMTUwIDc1IDAuMAp2IDE3NSA3NSAwLjAKdiAyMDAgNzUgMC4wCnYgMjI1IDc1IDAuMAp2IDI1MCA3NSAwLjAKdiAyNzUgNzUgMC4wCnYgMCAxMDAgMC4wCnYgMjUgMTAwIDAuMAp2IDUwIDEwMCAwLjAKdiA3NSAxMDAgMC4wCnYgMTAwIDEwMCAwLjAKdiAxMjUgMTAwIDAuMAp2IDE1MCAxMDAgMC4wCnYgMTc1IDEwMCAwLjAKdiAyMDAgMTAwIDAuMAp2IDIyNSAxMDAgMC4wCnYgMjUwIDEwMCAwLjAKdiAyNzUgMTAwIDAuMAp2IDAgMTI1IDAuMAp2IDI1IDEyNSAwLjAKdiA1MCAxMjUgMC4wCnYgNzUgMTI1IDAuMAp2IDEwMCAxMjUgMC4wCnYgMTI1IDEyNSAwLjAKdiAxNTAgMTI1IDAuMAp2IDE3NSAxMjUgMC4wCnYgMjAwIDEyNSAwLjAKdiAyMjUgMTI1IDAuMAp2IDI1MCAxMjUgMC4wCnYgMjc1IDEyNSAwLjAKdiAwIDE1MCAwLjAKdiAyNSAxNTAgMC4wCnYgNTAgMTUwIDAuMAp2IDc1IDE1MCAwLjAKdiAxMDAgMTUwIDAuMAp2IDEyNSAxNTAgMC4wCnYgMTUwIDE1MCAwLjAKdiAxNzUgMTUwIDAuMAp2IDIwMCAxNTAgMC4wCnYgMjI1IDE1MCAwLjAKdiAyNTAgMTUwIDAuMAp2IDI3NSAxNTAgMC4wCnYgMCAxNzUgMC4wCnYgMjUgMTc1IDAuMAp2IDUwIDE3NSAwLjAKdiA3NSAxNzUgMC4wCnYgMTAwIDE3NSAwLjAKdiAxMjUgMTc1IDAuMAp2IDE1MCAxNzUgMC4wCnYgMTc1IDE3NSAwLjAKdiAyMDAgMTc1IDAuMAp2IDIyNSAxNzUgMC4wCnYgMjUwIDE3NSAwLjAKdiAyNzUgMTc1IDAuMAp2IDAgMjAwIDAuMAp2IDI1IDIwMCAwLjAKdiA1MCAyMDAgMC4wCnYgNzUgMjAwIDAuMAp2IDEwMCAyMDAgMC4wCnYgMTI1IDIwMCAwLjAKdiAxNTAgMjAwIDAuMAp2IDE3NSAyMDAgMC4wCnYgMjAwIDIwMCAwLjAKdiAyMjUgMjAwIDAuMAp2IDI1MCAyMDAgMC4wCnYgMjc1IDIwMCAwLjAKdiAwIDIyNSAwLjAKdiAyNSAyMjUgMC4wCnYgNTAgMjI1IDAuMAp2IDc1IDIyNSAwLjAKdiAxMDAgMjI1IDAuMAp2IDEyNSAyMjUgMC4wCnYgMTUwIDIyNSAwLjAKdiAxNzUgMjI1IDAuMAp2IDIwMCAyMjUgMC4wCnYgMjI1IDIyNSAwLjAKdiAyNTAgMjI1IDAuMAp2IDI3NSAyMjUgMC4wCnYgMCAyNTAgMC4wCnYgMjUgMjUwIDAuMAp2IDUwIDI1MCAwLjAKdiA3NSAyNTAgMC4wCnYgMTAwIDI1MCAwLjAKdiAxMjUgMjUwIDAuMAp2IDE1MCAyNTAgMC4wCnYgMTc1IDI1MCAwLjAKdiAyMDAgMjUwIDAuMAp2IDIyNSAyNTAgMC4wCnYgMjUwIDI1MCAwLjAKdiAyNzUgMjUwIDAuMAp2IDAgMjc1IDAuMAp2IDI1IDI3NSAwLjAKdiA1MCAyNzUgMC4wCnYgNzUgMjc1IDAuMAp2IDEwMCAyNzUgMC4wCnYgMTI1IDI3NSAwLjAKdiAxNTAgMjc1IDAuMAp2IDE3NSAyNzUgMC4wCnYgMjAwIDI3NSAwLjAKdiAyMjUgMjc1IDAuMAp2IDI1MCAyNzUgMC4wCnYgMjc1IDI3NSAwLjAKdiAyNTAuMCAwLjAgMC4wCnYgMC4wIDEwLjAgMC4wCnYgMjUwLjAgMTAuMCAwLjAKdiAwLjAgMjAuMCAwLjAKdiAyNTAuMCAyMC4wIDAuMAp2IDAuMCAzMC4wIDAuMAp2IDI1MC4wIDMwLjAgMC4wCnYgMC4wIDQwLjAgMC4wCnYgMjUwLjAgNDAuMCAwLjAKdiAwLjAgNTAuMCAwLjAKdiAyNTAuMCA1MC4wIDAuMAp2IDAuMCA2MC4wIDAuMAp2IDI1MC4wIDYwLjAgMC4wCnYgMC4wIDcwLjAgMC4wCnYgMjUwLjAgNzAuMCAwLjAKdiAwLjAgODAuMCAwLjAKdiAyNDkuOTk5OTk5OTk5OTk5OTcgODAuMCAwLjAKdiAwLjAgOTAuMCAwLjAKdiAyNTAuMCA5MC4wIDAuMAp2IDAuMCAxMDAuMCAwLjAKdiAyNTAuMCAxMDAuMCAwLjAKdiAwLjAgMTEwLjAgMC4wCnYgMjUwLjAgMTEwLjAgMC4wCnYgMC4wIDEyMC4wIDAuMAp2IDI1MC4wIDEyMC4wIDAuMAp2IDAuMCAxMzAuMCAwLjAKdiAyNTAuMCAxMzAuMCAwLjAKdiAwLjAgMTQwLjAgMC4wCnYgMjUwLjAgMTQwLjAgMC4wCnYgMC4wIDE1MC4wIDAuMAp2IDI1MC4wIDE1MC4wIDAuMAp2IDAuMCAxNjAuMCAwLjAKdiAyNTAuMCAxNjAuMCAwLjAKdiAwLjAgMTcwLjAgMC4wCnYgMjUwLjAgMTcwLjAgMC4wCnYgMC4wIDE4MC4wIDAuMAp2IDI1MC4wIDE4MC4wIDAuMAp2IDAuMCAxOTAuMCAwLjAKdiAyNTAuMCAxOTAuMCAwLjAKdiAwLjAgMjAwLjAgMC4wCnYgMjUwLjAgMjAwLjAgMC4wCnYgMC4wIDIxMC4wIDAuMAp2IDI1MC4wIDIxMC4wIDAuMAp2IDAuMCAyMjAuMCAwLjAKdiAyNTAuMCAyMjAuMCAwLjAKdiAwLjAgMjMwLjAgMC4wCnYgMjUwLjAgMjMwLjAgMC4wCnYgMC4wIDI0MC4wIDAuMAp2IDI1MC4wIDI0MC4wIDAuMApmIDE0IDE1IDIKZiAxNSAxNiAzCmYgMTYgMTcgNApmIDE3IDE4IDUKZiAxOCAxOSA2CmYgMTkgMjAgNwpmIDIwIDIxIDgKZiAyMSAyMiA5CmYgMjIgMjMgMTAKZiAxNSAzIDIKZiAxNiA0IDMKZiAxNyA1IDQKZiAxOCA2IDUKZiAxOSA3IDYKZiAyMCA4IDcKZiAyMSA5IDgKZiAyMiAxMCA5CmYgMjYgMjcgMTQKZiAyNyAyOCAxNQpmIDI4IDI5IDE2CmYgMjkgMzAgMTcKZiAzMCAzMSAxOApmIDMxIDMyIDE5CmYgMzIgMzMgMjAKZiAzMyAzNCAyMQpmIDI2IDE0IDEzCmYgMjcgMTUgMTQKZiAyOCAxNiAxNQpmIDI5IDE3IDE2CmYgMzAgMTggMTcKZiAzMSAxOSAxOApmIDMyIDIwIDE5CmYgMzMgMjEgMjAKZiAzNCAyMiAyMQpmIDM2IDI0IDIzCmYgMzggMzkgMjYKZiAzOSA0MCAyNwpmIDQwIDQxIDI4CmYgNDEgNDIgMjkKZiA0MiA0MyAzMApmIDQzIDQ0IDMxCmYgNDQgNDUgMzIKZiA0NSA0NiAzMwpmIDQ2IDQ3IDM0CmYgMzkgMjcgMjYKZiA0MCAyOCAyNwpmIDQxIDI5IDI4CmYgNDIgMzAgMjkKZiA0MyAzMSAzMApmIDQ0IDMyIDMxCmYgNDUgMzMgMzIKZiA0NiAzNCAzMwpmIDUwIDUxIDM4CmYgNTEgNTIgMzkKZiA1MiA1MyA0MApmIDUzIDU0IDQxCmYgNTQgNTUgNDIKZiA1NSA1NiA0MwpmIDU2IDU3IDQ0CmYgNTcgNTggNDUKZiA1MCAzOCAzNwpmIDUxIDM5IDM4CmYgNTIgNDAgMzkKZiA1MyA0MSA0MApmIDU0IDQyIDQxCmYgNTUgNDMgNDIKZiA1NiA0NCA0MwpmIDU3IDQ1IDQ0CmYgNTggNDYgNDUKZiA2MCA0OCA0NwpmIDYyIDYzIDUwCmYgNjMgNjQgNTEKZiA2NCA2NSA1MgpmIDY1IDY2IDUzCmYgNjYgNjcgNTQKZiA2NyA2OCA1NQpmIDY4IDY5IDU2CmYgNjkgNzAgNTcKZiA3MCA3MSA1OApmIDYzIDUxIDUwCmYgNjQgNTIgNTEKZiA2NSA1MyA1MgpmIDY2IDU0IDUzCmYgNjcgNTUgNTQKZiA2OCA1NiA1NQpmIDY5IDU3IDU2CmYgNzAgNTggNTcKZiA3NCA3NSA2MgpmIDc1IDc2IDYzCmYgNzYgNzcgNjQKZiA3NyA3OCA2NQpmIDc4IDc5IDY2CmYgNzkgODAgNjcKZiA4MCA4MSA2OApmIDgxIDgyIDY5CmYgNzQgNjIgNjEKZiA3NSA2MyA2MgpmIDc2IDY0IDYzCmYgNzcgNjUgNjQKZiA3OCA2NiA2NQpmIDc5IDY3IDY2CmYgODAgNjggNjcKZiA4MSA2OSA2OApmIDgyIDcwIDY5CmYgODQgNzIgNzEKZiA4NiA4NyA3NApmIDg3IDg4IDc1CmYgODggODkgNzYKZiA4OSA5MCA3NwpmIDkwIDkxIDc4CmYgOTEgOTIgNzkKZiA5MiA5MyA4MApmIDkzIDk0IDgxCmYgOTQgOTUgODIKZiA4NyA3NSA3NApmIDg4IDc2IDc1CmYgODkgNzcgNzYKZiA5MCA3OCA3NwpmIDkxIDc5IDc4CmYgOTIgODAgNzkKZiA5MyA4MSA4MApmIDk0IDgyIDgxCmYgOTggOTkgODYKZiA5OSAxMDAgODcKZiAxMDAgMTAxIDg4CmYgMTAxIDEwMiA4OQpmIDEwMiAxMDMgOTAKZiAxMDMgMTA0IDkxCmYgMTA0IDEwNSA5MgpmIDEwNSAxMDYgOTMKZiA5OCA4NiA4NQpmIDk5IDg3IDg2CmYgMTAwIDg4IDg3CmYgMTAxIDg5IDg4CmYgMTAyIDkwIDg5CmYgMTAzIDkxIDkwCmYgMTA0IDkyIDkxCmYgMTA1IDkzIDkyCmYgMTA2IDk0IDkzCmYgMTA4IDk2IDk1CmYgMTEwIDExMSA5OApmIDExMSAxMTIgOTkKZiAxMTIgMTEzIDEwMApmIDExMyAxMTQgMTAxCmYgMTE0IDExNSAxMDIKZiAxMTUgMTE2IDEwMwpmIDExNiAxMTcgMTA0CmYgMTE3IDExOCAxMDUKZiAxMTggMTE5IDEwNgpmIDExMSA5OSA5OApmIDExMiAxMDAgOTkKZiAxMTMgMTAxIDEwMApmIDExNCAxMDIgMTAxCmYgMTE1IDEwMyAxMDIKZiAxMTYgMTA0IDEwMwpmIDExNyAxMDUgMTA0CmYgMTE4IDEwNiAxMDUKZiAxMjIgMTIzIDExMApmIDEyMyAxMjQgMTExCmYgMTI0IDEyNSAxMTIKZiAxMjUgMTI2IDExMwpmIDEyNiAxMjcgMTE0CmYgMTI3IDEyOCAxMTUKZiAxMjggMTI5IDExNgpmIDEyOSAxMzAgMTE3CmYgMTMwIDEzMSAxMTgKZiAxMjIgMTEwIDEwOQpmIDEyMyAxMTEgMTEwCmYgMTI0IDExMiAxMTEKZiAxMjUgMTEzIDExMgpmIDEyNiAxMTQgMTEzCmYgMTI3IDExNSAxMTQKZiAxMjggMTE2IDExNQpmIDEyOSAxMTcgMTE2CmYgMTMwIDExOCAxMTcKZiAxMzIgMTIwIDExOQpmIDEzMyAxMzQgMTIxCmYgMTM0IDEzNSAxMjIKZiAxMzUgMTM2IDEyMwpmIDEzNiAxMzcgMTI0CmYgMTM3IDEzOCAxMjUKZiAxMzggMTM5IDEyNgpmIDEzOSAxNDAgMTI3CmYgMTQwIDE0MSAxMjgKZiAxNDEgMTQyIDEyOQpmIDE0MiAxNDMgMTMwCmYgMTQzIDE0NCAxMzEKZiAxMzQgMTIyIDEyMQpmIDEzNSAxMjMgMTIyCmYgMTM2IDEyNCAxMjMKZiAxMzcgMTI1IDEyNApmIDEzOCAxMjYgMTI1CmYgMTM5IDEyNyAxMjYKZiAxNDAgMTI4IDEyNwpmIDE0MSAxMjkgMTI4CmYgMTQyIDEzMCAxMjkKZiAxNDMgMTMxIDEzMApmIDE0NCAxMzIgMTMxCmYgMSAxNCAyCmYgMTQ1IDI0IDEyCmYgMTQ2IDEgMTQKZiAxNDcgMTQ1IDI0CmYgMTQ3IDE0NSAxMApmIDE0OCAxMyAxNApmIDE0OCAxNDYgMTQKZiAxNDkgMjMgMjQKZiAxNDkgMTQ3IDI0CmYgMTQ5IDIzIDEwCmYgMTQ5IDE0NyAxMApmIDE1MCAyNiAxMwpmIDE1MSAzNiAyMwpmIDE1MSAyMyAyMgpmIDE1MiAxNTAgMjYKZiAxNTMgMTUxIDM2CmYgMTUzIDE1MSAyMgpmIDE1NCAzOCAyNgpmIDE1NCAxNTIgMjYKZiAxNTUgMzQgMjIKZiAxNTUgNDggMzYKZiAxNTUgMTUzIDM2CmYgMTU1IDE1MyAyMgpmIDE1NiAxNTQgMzgKZiAxNTcgMTU1IDQ4CmYgMTU3IDE1NSAzNApmIDE1OCAzNyAzOApmIDE1OCAxNTYgMzgKZiAxNTkgNDcgNDgKZiAxNTkgMTU3IDQ4CmYgMTU5IDQ3IDM0CmYgMTU5IDE1NyAzNApmIDE2MCA1MCAzNwpmIDE2MSA0NyA0NgpmIDE2MiAxNjAgNTAKZiAxNjMgNjAgNDcKZiAxNjQgNjIgNTAKZiAxNjQgMTYyIDUwCmYgMTY1IDU4IDQ2CmYgMTY1IDcyIDYwCmYgMTY1IDE2MSA0NgpmIDE2NSAxNjMgNjAKZiAxNjYgMTY0IDYyCmYgMTY3IDE2NSA3MgpmIDE2NyAxNjUgNTgKZiAxNjggNjEgNjIKZiAxNjggMTY2IDYyCmYgMTY5IDcxIDcyCmYgMTY5IDE2NyA3MgpmIDE2OSA3MSA1OApmIDE2OSAxNjcgNTgKZiAxNzAgNzQgNjEKZiAxNzEgODQgNzEKZiAxNzEgNzEgNzAKZiAxNzIgMTcwIDc0CmYgMTczIDE3MSA4NApmIDE3MyAxNzEgNzAKZiAxNzQgODYgNzQKZiAxNzQgMTcyIDc0CmYgMTc1IDgyIDcwCmYgMTc1IDk2IDg0CmYgMTc1IDE3MyA4NApmIDE3NSAxNzMgNzAKZiAxNzYgMTc0IDg2CmYgMTc3IDE3NSA5NgpmIDE3NyAxNzUgODIKZiAxNzggODUgODYKZiAxNzggMTc2IDg2CmYgMTc5IDk1IDk2CmYgMTc5IDE3NyA5NgpmIDE3OSA5NSA4MgpmIDE3OSAxNzcgODIKZiAxODAgOTggODUKZiAxODEgMTA4IDk1CmYgMTgxIDk1IDk0CmYgMTgyIDE4MCA5OApmIDE4MyAxODEgMTA4CmYgMTgzIDE4MSA5NApmIDE4NCAxMTAgOTgKZiAxODQgMTgyIDk4CmYgMTg1IDEwNiA5NApmIDE4NSAxMjAgMTA4CmYgMTg1IDE4MyAxMDgKZiAxODUgMTgzIDk0CmYgMTg2IDE4NCAxMTAKZiAxODcgMTg1IDEyMApmIDE4NyAxODUgMTA2CmYgMTg4IDEwOSAxMTAKZiAxODggMTg2IDExMApmIDE4OSAxMTkgMTIwCmYgMTg5IDE4NyAxMjAKZiAxODkgMTE5IDEwNgpmIDE4OSAxODcgMTA2CmYgMTkwIDEyMiAxMDkKZiAxOTEgMTMyIDExOQpmIDE5MSAxMTkgMTE4CmYgMTkyIDEyMSAxMjIKZiAxOTIgMTkwIDEyMgpmIDE5MyAxMzEgMTMyCmYgMTkzIDE5MSAxMzIKZiAxOTMgMTMxIDExOApmIDE5MyAxOTEgMTE4CmwgMSAxNDUKbCAxNDYgMTQ3CmwgMTQ4IDE0OQpsIDE1MCAxNTEKbCAxNTIgMTUzCmwgMTU0IDE1NQpsIDE1NiAxNTcKbCAxNTggMTU5CmwgMTYwIDE2MQpsIDE2MiAxNjMKbCAxNjQgMTY1CmwgMTY2IDE2NwpsIDE2OCAxNjkKbCAxNzAgMTcxCmwgMTcyIDE3MwpsIDE3NCAxNzUKbCAxNzYgMTc3CmwgMTc4IDE3OQpsIDE4MCAxODEKbCAxODIgMTgzCmwgMTg0IDE4NQpsIDE4NiAxODcKbCAxODggMTg5CmwgMTkwIDE5MQpsIDE5MiAxOTMK





    
![svg](readme_files/readme_76_1.svg)
    



## Making a skirt for myself

I would like a skirt. To get one, I’ve measured my body a little bit:


```python
joelle_waist = 725
joelle_hips = 900
joelle_waist_to_hips = 265
```

I’ve also decided a few dimensions of the skirt I’d like to make:


```python
skirt_length_below_the_hips = 380
skirt_bottom_circumference = 1200
```

Here is a graph plotting the circumference of the skirt over height:


```python
from src.geometry.Shape import measurement_from_y_axis
skirt_circumference_graph = Shape()

origin = Vector(0,0)
waist_point = Vector(joelle_waist, 0)
hips_point = Vector(joelle_hips, -joelle_waist_to_hips)
hem_point = Vector(skirt_bottom_circumference, -joelle_waist_to_hips - skirt_length_below_the_hips)

skirt_circumference_graph.lineTo(waist_point)
skirt_circumference_graph.lineTo(hips_point)
skirt_circumference_graph.lineTo(hem_point)

render(
  skirt_circumference_graph.close_against_y_axis(),
  origin,
  measurement_from_y_axis(waist_point),
  measurement_from_y_axis(hips_point),
  measurement_from_y_axis(hem_point)
  )

```




    
![svg](readme_files/readme_82_0.svg)
    



This is the circumference of the skirt over elevation. But I think what
I need (in order to get the scrolled hem I’m looking for) is the radius.
To keep it simple I’ll imagine the skirt as a circlular prism with
radius varying across its length.


```python
skirt_radius_graph = Shape([Vector(p.x / (2*math.pi),  p.y) for p in skirt_circumference_graph.points])
render(skirt_radius_graph)
```




    
![svg](readme_files/readme_84_0.svg)
    



This is a reasonable approximation for the silhouette of the skirt.

Now I’ll add the scroll


```python
skirt_radius_graph.continue_with_arc(175, 2*math.pi)
render(skirt_radius_graph)
```




    
![svg](readme_files/readme_86_0.svg)
    



Here’s what it should look like in 3d:


```python
render(*[
  skirt_radius_graph.to_3D().rotate(pitch=angle).isometric() for angle in np.arange(0, math.pi*2, .1)
])
```




    
![svg](readme_files/readme_88_0.svg)
    



Now I’ve found a silhouette I like, I’ll unwrap this by length onto the
y-axis.


```python
final_radius_graph = Shape()
for w in np.arange(0, skirt_radius_graph.length, 10):
  x = skirt_radius_graph.pointAlong(w).x
  p = Vector(x, -w)
  final_radius_graph.lineTo(p)
render(final_radius_graph.close_against_y_axis())
```




    
![svg](readme_files/readme_90_0.svg)
    



Next we transform this back into a circumference graph


```python
final_circumference_graph = Shape(
  [Vector(x = p.x * 2*math.pi, y=p.y) for p in final_radius_graph.points]
)

render(final_circumference_graph.close_against_y_axis())
```




    
![svg](readme_files/readme_92_0.svg)
    



Wow mad. Finally, lets subdivide this into 10 pattern pieces:


```python
pattern_shape = final_circumference_graph.close_against_y_axis().subdivide_by_width(10)
render(pattern_shape)
```




    
![svg](readme_files/readme_94_0.svg)
    



Now I just need to add some seam & hem allowances. While I’m at it, I’ll
make a pattern for the boning channel.


```python
from src.geometry.Shape import rectangle

pattern_piece = Group(
  shape=pattern_shape,
  right_side = pattern_shape.sides()[0].with_style("line"),
  left_side = pattern_shape.sides()[2].with_style("line").reverse(),
  right_allowance = pattern_shape.sides()[0].allowance(-20),
  left_allowance = pattern_shape.sides()[2].allowance(-20),
  center_line = pattern_shape.vertical_center_line(),
)

boning = rectangle(pattern_shape.x_center() - 6, pattern_shape.bottom, 12, pattern_shape.height).with_label("12mm boning channel")

render(
  *sideBySide(
    pattern_piece,
    Group(
      boning,
      boning.allowance(-12)
    )
  )
)
```




    
![svg](readme_files/readme_96_0.svg)
    



Here is a demo of the construction in 3D:


```python
pattern_piece_3d = pattern_piece.to_3D()
pieces = []
for phase in np.arange(0, 1, 1.0/10.0):
  pieces.append(pattern_piece_3d.translate(z=1000).rotate(pitch=phase * 2 * math.pi).isometric())

from src.geometry.seam_lines import seam_lines

all = []
for i in range(len(pieces)):
  a = pieces[i]
  b = pieces[(i+1)%len(pieces)]
  all.append(a)
  all.append(seam_lines(a["left_side"], b["right_side"]))

render(*all)
```




    
![svg](readme_files/readme_98_0.svg)
    


