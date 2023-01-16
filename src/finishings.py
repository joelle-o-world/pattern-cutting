from src.geometry.Shape import Shape
from src.geometry.Group import Group

def rolled_hem(edge: Shape, amount: float):
    allowance = edge.allowance(amount * 1.75)
    fold_line = edge.parallel(amount)
    return Group(allowance, fold_line)

