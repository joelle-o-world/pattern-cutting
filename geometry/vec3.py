class vec3:
    "Cartesian coordinate/vector with 3 dimensions"

    x: float
    y: float
    z: float

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)
