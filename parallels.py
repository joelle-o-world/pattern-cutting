from DieLemmaDressBlock import shape as DieLemmaDressBlock
from render import render
from geometry.LineSegment import LineSegment

hemAllowance = DieLemmaDressBlock.parallel(50)


projectionLines = [LineSegment(p1, p2) for p1, p2 in zip(DieLemmaDressBlock.points, hemAllowance.points)]

parallelLineSegments = [segment.parallel(50) for segment in DieLemmaDressBlock.segments()]

render([
    DieLemmaDressBlock,
    *DieLemmaDressBlock.points,  
    *projectionLines, 
    # *parallelLineSegments,
    hemAllowance
]).saveSvg("Testing parallel.svg")



