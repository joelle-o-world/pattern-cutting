import drawSvg as svg
from src.geometry.Abstract_Group import Abstract_Group
from src.geometry.Vector import Vector

from src.geometry.isMovable import isMovable


class Group(Abstract_Group):

    label: str | None

    def __init__(self, *objects, **kwargs):
        self.objects = {}
        self.label = None
        for key in kwargs:
            self[key] = kwargs[key]

        for object in objects:
            self.append(object)

    @property
    def left(self) -> float:
        return min([obj.left for obj in self.iterate_objects()])

    @property
    def right(self) -> float:
        return max([obj.right for obj in self.iterate_objects()])

    @property
    def top(self) -> float:
        return max([obj.top for obj in self.iterate_objects()])

    @property
    def bottom(self) -> float:
        return min([obj.bottom for obj in self.iterate_objects()])

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.top - self.bottom

    def midpoint(self):
        sum = Vector(0, 0)
        for name in self.objects:
            sum += self.objects[name].midpoint()
        return sum / len(self.objects)

    def svg_label(self):
        if self.label:
            midpoint = self.midpoint()
            return svg.Text(
                self.label, 12, midpoint.x, midpoint.y, fill="#000000", stroke="none"
            )

    def svg(self):
        g = svg.Group([obj.svg() for obj in self.iterate_objects()])
        label = self.svg_label()
        if label:
            g.append(label)
        return g

    def move(self, x: float, y: float):
        return Group(
            *[
                obj.move(x, y) if isMovable(obj) else obj
                for obj in self.iterate_objects()
            ]
        )

    def to_3D(self):
        from src.geometry.Group3d import Group3d

        g = Group3d()
        for name in self.objects:
            g[name] = self.objects[name].to_3D()
        return g
