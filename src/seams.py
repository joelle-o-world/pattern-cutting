from src.geometry.Shape import Shape
from src.geometry.Group import Group
from src.notches import notch_on_shape
from src.units import inch


def french_seam_allowance(
    a: Shape, seam_allowance=1 * inch, notch_positions: list[float] | None = None
):
    fold_allowance = 0.6 * seam_allowance

    if not notch_positions:
        # TODO: Use notches at regular intervals
        notch_positions = [50]

    notches = Group()
    for notch_position in notch_positions:
        notch = notch_on_shape(a, notch_position, length=seam_allowance)
        notches.append(notch)

    return Group(
        allowance=a.allowance(seam_allowance),
        fold=a.parallel(fold_allowance).with_style("dashed"),
        notches=notches,
    )


def french_seam(a: Shape, b: Shape, seam_allowance=1 * inch):
    if a.length != b.length:
        print(
            "Warning: creating french seam on two lines with different length: {} and {}".format(
                a.length, b.length
            )
        )

    return Group(
        a=french_seam_allowance(a, seam_allowance),
        b=french_seam_allowance(b, seam_allowance),
    )
