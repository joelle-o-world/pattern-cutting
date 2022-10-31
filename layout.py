def layout(objects, margin = 25):
    x = margin
    for object in objects:
        yield object.move(x-object.left, margin-object.bottom)
        x += object.width 
        x += margin


def topToBottom(*objects, margin = 50):
    y = margin
    l = []
    for object in objects:
        l.append( object.move(margin-object.left, y-object.top))
        y -= object.height 
        y -= margin

    return l

def sideBySide(*objects, margin = 25):
    x = margin
    l = []
    for object in objects:
        l.append( object.move(x-object.left, margin-object.bottom))
        x += object.width 
        x += margin

    return l
