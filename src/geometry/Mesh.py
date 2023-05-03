from .Shape import Shape
from src.geometry.Group import Group
from src.geometry.Vector import Vector


class Mesh:
    def __init__(self, vertices=[], faces=[], lines=[]):
        self.vertices = vertices
        self.lines = lines
        self.faces = faces

    def read_vertex_2d(self, index):
        return Vector(x=self.vertices[index][0], y=self.vertices[index][1])

    def add_vertex(self, x, y, z=0.0):
        self.vertices.append((x, y, z))
        return len(self.vertices) - 1

    def delete_vertex(self, index: int):
        del self.vertices[index]
        def f(i):
            "Update vertex index"
            return i if i < index else i - 1
        self.faces = [(f(a), f(b), f(c)) for a,b,c in self.faces if a != index and b != index and c != index]
        self.lines = [(f(a), f(b)) for a , b in self.lines if a != index and b != index]

    def update_vertex(self, index, x: float, y: float, z=0.0):
        self.vertices[index] = [x, y, z]

    def add_face(self, a, b, c):
        if a != None and b != None and c != None:
            self.faces.append((a, b, c))

    def obj_str(self):
        str = ""
        for x, y, z in self.vertices:
            str += "v {} {} {}\n".format(x, y, z)
        for a, b, c in self.faces:
            str += "f {} {} {}\n".format(a, b, c)
        for a, b in self.lines:
            str += "l {} {}\n".format(a, b)
        return str

    def isometric(self):
        points = [
            Vector(x=point[0] + point[2] * 0.5, y=point[1] + point[2] * 0.5)
            for point in self.vertices
        ]
        faces = [
            Shape([points[face[0]], points[face[1]], points[face[2]]])
            for face in self.faces
        ]
        lines = [Shape([points[line[0]], points[line[1]]]) for line in self.lines]
        return Group(*faces, *lines)
