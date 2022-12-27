import drawSvg as svg

from src.geometry.isMovable import isMovable


class Group:
    label = None

    def __init__(self, *objects, **kwargs):
        self.objects = {}
        for key in kwargs:
            self[key] = kwargs[key]

        for object in objects:
            self.append(object)

    def new_unused_key(self, prefix="unlabeled_"):
        i = 0
        while "{}{}".format(prefix, i) in self.objects:
            i += 1
        return "{}{}".format(prefix, i)

    def __getitem__(self, key: str):
        return self.objects[key]
    def __setitem__(self, key: str, value):
        self.objects[key ] = value
    def __delitem__(self, key):
        del self.objects[key]

    def append(self, obj):
        self.objects[self.new_unused_key()] = obj

    def iterate_objects(self):
        for key in self.objects:
            yield self.objects[key]

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

    def svg(self):
        return svg.Group([obj.svg() for obj in self.iterate_objects()])

    def move(self, x: float, y: float):
        return Group(
            *[obj.move(x, y) if isMovable(obj) else obj for obj in self.iterate_objects()]
        )
