import numpy as np

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

    @property
    def matrix(self):
        return [self.x, self.y, self.z, 1.0]

    def transform(self, matrix):
        m = np.matmul(self.matrix,  matrix)
        return vec3(x = m[0], y=m[1], z=m[2])
        
