import pytest

from c01_w02_counting_inversions import sort_and_count


INVERSION_CASES = [
    ([1, 3, 5, 2, 4, 6], (3, [1, 2, 3, 4, 5, 6])),
    ([1, 2, 3], (0, [1, 2, 3])),
    ([3, 2, 1], (3, [1, 2, 3])),
    ([2, 1], (1, [1, 2])),
]
@pytest.mark.parametrize("input_list,expected_output", INVERSION_CASES)
def test_sort_and_count(input_list, expected_output):
    assert sort_and_count(input_list) == expected_output
