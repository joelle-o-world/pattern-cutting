from math import radians

import pytest

from pattern_cutting.geometry.angles import normalize_angle


@pytest.mark.parametrize(
    "angle_deg, expected_angle_deg",
    [
        (0, 0),
        (60, 60),
        (180, 180),
        (270, -90),
        (-270, 90),
    ],
)
def test_normalize_angle(angle_deg, expected_angle_deg):
    angle = radians(angle_deg)
    assert normalize_angle(angle) == radians(expected_angle_deg)


def test_clockwise_difference():
    pass
