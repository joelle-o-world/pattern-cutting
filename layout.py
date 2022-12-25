from src.geometry.Vector import Vector
from src.geometry.Shape import arrow


def layout(objects, margin=25):
    x = margin
    for object in objects:
        yield object.move(x - object.left, margin - object.bottom)
        x += object.width
        x += margin


def topToBottom(*objects, margin=50):
    y = margin
    l = []
    for object in objects:
        l.append(object.move(margin - object.left, y - object.top))
        y -= object.height
        y -= margin

    return l


def side_by_side(*objects, margin=25):
    x = margin
    l = []
    for object in objects:
        print(object.label, object.width)
        l.append(object.move(x - object.left, margin - object.top))
        x += object.width
        x += margin

    return l
def sideBySide(*objects, margin=25):
    "deprecated alias for side_by_side"
    return side_by_side(*objects, margin=margin)


def process(*objects):
    l = []
    then = arrow(Vector(0, 0), Vector(30, 0))
    for o in objects[:-1]:
        l.append(o)
        l.append(then)
    l.append(objects[-1])
    return sideBySide(*l, margin=75)
