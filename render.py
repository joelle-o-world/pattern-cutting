import drawSvg as draw

from src.geometry.Rectangle import minimumBoundingRect


def render(*objects):
    "Quickly render any number of objects as SVG"

    rect = minimumBoundingRect(objects)

    # Add a margin
    rect = rect.enlarge(100)

    d = draw.Drawing(rect.width, rect.height, origin=(rect.left,rect.bottom), stroke='black', fill='none')
    
    for object in objects:
        d.append(object.svg())

    return d


