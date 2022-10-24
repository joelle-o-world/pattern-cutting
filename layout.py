def layout(objects, margin = 25):
    x = margin
    for object in objects:
        yield object.move(x-object.left, margin-object.bottom)
        x += object.width 
        x += margin

