import drawSvg as svg

from src.geometry.isMovable import isMovable


class Group:
    label = None

    def __init__(self, *objects):
        self.objects = objects

    def append(self, obj):
        self.objects.append(obj)

    @property
    def left(self) -> float:
        return min([obj.left for obj in self.objects])

    @property
    def right(self) -> float:
        return max([obj.right for obj in self.objects])

    @property
    def top(self) -> float:
        return max([obj.top for obj in self.objects])

    @property
    def bottom(self) -> float:
        return min([obj.bottom for obj in self.objects])

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.top - self.bottom

    def svg(self):
        return svg.Group([obj.svg() for obj in self.objects])

    def move(self, x: float, y: float):
        return Group(
            *[obj.move(x, y) if isMovable(obj) else obj for obj in self.objects]
        )
