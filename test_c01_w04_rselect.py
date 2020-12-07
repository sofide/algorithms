import pytest

from c01_w04_rselect import rselect


RSELECT_CASES = [
    ([1, 143, 42, 23, 4], 1, 1),
    ([1, 143, 42, 23, 4], 2, 4),
    ([1, 143, 42, 23, 4], 3, 23),
    ([1, 143, 42, 23, 4], 4, 42),
    ([1, 143, 42, 23, 4], 5, 143),
]
@pytest.mark.parametrize("array,index,expected_value", RSELECT_CASES)
def test_rselect(array, index, expected_value):
    assert rselect(array, index) == expected_value
