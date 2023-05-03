from src.geometry.triangle import triangle_point_collision
import math
import numpy as np
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

        self.faces = [
            (f(a), f(b), f(c))
            for a, b, c in self.faces
            if a != index and b != index and c != index
        ]
        self.lines = [(f(a), f(b)) for a, b in self.lines if a != index and b != index]

    def update_vertex(self, index, x: float, y: float, z=0.0):
        self.vertices[index] = (x, y, z)

    def closest_vertex_to(self, p):
        self.assert_flat()
        # TODO: generalise for 3 dimensions
        distances = [distance(p, q) for q in self.vertices]
        smallest_disance = min(distances)
        return distances.index(smallest_disance)

    def vertex_at_point(self, p, tolerance=0.0):
        self.assert_flat()
        # TODO: generalise for 3 dimensions
        if tolerance != 0:
            closest_index = self.closest_vertex_to(p)
            closest_point = self.read_vertex_2d(closest_index)
            if distance(p, closest_point) < tolerance:
                return closest_index
            else:
                return None
        else:
            for i, (x, y) in enumerate(self.vertices):
                if x == p[0] and y == y[1]:
                    return i
            # Otherwise
            return None

    def add_face(self, a, b, c):
        self.assert_flat()
        if a != None and b != None and c != None:
            self.faces.append((a, b, c))

    def face_coordinates(self, index):
        "Get the coordinates of a single face by index"
        a, b, c = self.faces[index]
        return self.vertices[a], self.vertices[b], self.vertices[c]

    def faces_colliding_with_point(self, p):
        for face_index, (a, b, c) in enumerate(self.faces):
            triangle = (self.vertices[a], self.vertices[b], self.vertices[c])
            if triangle_point_collision(triangle, p):
                yield face_index

    def is_flat(self):
        "In a flat mesh all vertices are on the plane z=0"
        for _, _, z in self.vertices:
            if z != 0:
                return False
        # otherwise
        return True

    def assert_flat(self):
        if not self.is_flat():
            raise Exception("Expected a flat mesh")

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
            Shape([points[face[0]], points[face[1]], points[face[2]]]).close()
            for face in self.faces
        ]
        lines = [Shape([points[line[0]], points[line[1]]]) for line in self.lines]
        return Group(*faces, *lines)

    @property
    def left(self):
        return min([x for x, _, _ in self.vertices])

    @property
    def right(self):
        return max([x for x, _, _ in self.vertices])

    @property
    def bottom(self):
        return min([y for _, y, _ in self.vertices])

    @property
    def top(self):
        return max([y for _, y, _ in self.vertices])

    def svg(self):
        return self.isometric().svg()


def mesh_grid(left, top, right=0, bottom=0, cell_size=25):
    mesh = Mesh()

    previous_row = None
    for y in np.arange(min(top, bottom), max(top, bottom), cell_size):
        current_row = [
            mesh.add_vertex(x, y)
            for x in np.arange(min(left, right), max(left, right), cell_size)
        ]
        if previous_row != None:
            for a, b, c in zip(current_row, current_row[1:], previous_row):
                mesh.add_face(a, b, c)
            for a, b, c in zip(current_row[1:], previous_row[1:], previous_row):
                mesh.add_face(a, b, c)

        previous_row = current_row

    return mesh


def distance(a, b):
    xa, ya = a
    xb, yb = b
    return math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
