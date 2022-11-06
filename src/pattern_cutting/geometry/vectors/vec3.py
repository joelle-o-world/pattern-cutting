class vec3:
    "Cartesian coordinate/vector with 3 dimensions"

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    x: float
    y: float
    z: float

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)
