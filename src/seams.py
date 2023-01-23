from src.geometry.Shape import Shape
from src.geometry.Group import Group
from src.units import inch


def french_seam_allowance(a: Shape, seam_allowance=1 * inch):
    fold_allowance = 0.6 * seam_allowance
    return Group(
        allowance=a.allowance(seam_allowance),
        fold=a.parallel(fold_allowance).with_style("dashed"),
    )


def french_seam(a: Shape, b: Shape, seam_allowance=1 * inch):

    # TODO: Add notches

    return Group(
        a=french_seam_allowance(a, seam_allowance),
        b=french_seam_allowance(b, seam_allowance),
    )
