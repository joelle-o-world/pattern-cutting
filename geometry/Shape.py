import numpy as np
import numpy.typing as npt
import drawSvg as svg

def project(point) -> tuple[float, float]:
    return (point[0], point[1])

class Shape:
    points: npt.NDArray
    close: bool
    def __init__(self, points, close=False):
        points = np.array(points)
        points = points.reshape(int(points.size/3), 3)
        self.points = points
        self.close = close

    def project2d(self):
        list = []
        for point in self.points:
            projected = project(point)
            list.append(projected[0])
            list.append(projected[1])
        return list

    def svg(self, ctx=None):
        if self.points.shape[0] == 1:
            # Render as a point
            dot = svg.Circle(*project(self.points[0]), 1, fill="black")
            return dot
        elif self.points.shape[0] > 1:
            # Render as a multisegment line
            return svg.Lines(*self.project2d(), close=self.close, stroke="#000000", fill="none")
