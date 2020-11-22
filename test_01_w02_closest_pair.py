import pytest

from c01_w02_closest_pair import get_closest_pair


CLOSEST_PAIR_CASES = [
    ([(1, 2), (3, 4)], ((1, 2), (3, 4))),
    ([(1, 2), (30, 40), (2, 3)], ((1, 2), (2, 3))),
    ([(1, 2), (30, 40), (1, 3)], ((1, 2), (1, 3))),
    ([(1, 2), (30, 40), (1, 3), (100, 200), (100, 100), (200, 200), (100.1, 100)], ((100, 100), (100.1, 100))),
]
@pytest.mark.parametrize("points,expected_result", CLOSEST_PAIR_CASES)
def test_get_closest_pair(points, expected_result):
    points_by_x = sorted(points, key= lambda x: x[0])
    points_by_y = sorted(points, key= lambda x: x[1])

    assert get_closest_pair(points_by_x, points_by_y) == expected_result
