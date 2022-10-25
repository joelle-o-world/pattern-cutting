from geometry.Rectangle import minimumBoundingRect
import drawSvg as draw

def render(*objects):
    "Quickly render any number of objects as SVG"

    rect = minimumBoundingRect(objects)

    # Add a margin
    rect = rect.enlarge(30)

    d = draw.Drawing(rect.width, rect.height, origin=(rect.left,rect.bottom), stroke='black', fill='none')
    
    for object in objects:
        d.append(object.svg())

    return d


