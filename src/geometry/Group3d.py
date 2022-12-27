from src.geometry.Abstract_Group import Abstract_Group
from src.geometry.Group import Group
from src.geometry.matrix_transformations import general_rotation, translate


class Group3d(Abstract_Group):
    def isometric(self):
        g = Group()
        for name in self.objects:
            g[name] = self[name].isometric()
        return g

    def transform(self, matrix):
        g = Group3d()
        for name in self.objects:
            g[name] = self[name].transform(matrix)
        return g

    def rotate(self, yaw=0.0, pitch=0.0, roll=0.0):
        matrix = general_rotation(yaw, pitch, roll)
        return self.transform(matrix)

    def translate(self, x=0.0, y=0.0, z=0.0):
        matrix = translate(x, y, z)
        return self.transform(matrix)
