class Rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self. top = top
        self.right = right
        self.bottom = bottom

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.top - self.bottom

    def enlarge(self, margin):
        "Create a new enlarged rectangle with margin added to all sides"
        return Rectangle(
                top = self.top + margin,
                bottom = self.bottom - margin,
                left = self.left - margin,
                right = self.right + margin
            )

def minimumBoundingRect(objects) -> Rectangle:
    "Find the minimum bounds rectangle of many objects"
    return Rectangle(
            top = max([object.top for object in objects]),
            bottom = min([object.bottom for object in objects]),
            left = min([object.left for object in objects]),
            right = max([object.right for object in objects])
        )
