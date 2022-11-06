def isMovable(shape):
    move_method = getattr(shape, "move", None)
    if callable(move_method):
        return True
    else:
        return False
