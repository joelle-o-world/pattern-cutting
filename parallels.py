from DieLemmaDressBlock import shape as DieLemmaDressBlock
from render import render
from geometry.LineSegment import LineSegment

hemAllowance = DieLemmaDressBlock.parallel(50)


projectionLines = [LineSegment(p1, p2) for p1, p2 in zip(DieLemmaDressBlock.points, hemAllowance.points)]

render([DieLemmaDressBlock, *DieLemmaDressBlock.points,  hemAllowance, *hemAllowance.points, *projectionLines]).saveSvg("Testing parallel.svg")



