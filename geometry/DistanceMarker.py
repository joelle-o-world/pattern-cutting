from geometry.PolyLine import PolyLine
import drawSvg as svg

class DistanceMarker(PolyLine):

    def startNotchSvg(self):
        first = self.firstSegment()
        vec = first.unitVector().normal().withLength(2)
        start = first.start + vec
        end = first.start - vec
        return svg.Line(start.x, start.y, end.x, end.y, stroke="#000000")

    def endNotchSvg(self):
        last = self.lastSegment()
        vec = last.unitVector().normal().withLength(2)
        start = last.end + vec
        end = last.end - vec
        return svg.Line(start.x, start.y, end.x, end.y, stroke="#000000")

    def svg(self):
        group = svg.Group()
        group.append(super().svg())
        group.append(self.startNotchSvg())
        group.append(self.endNotchSvg())
        return group

    def labelText(self):
        return "{:.1f}mm".format(self.length)


