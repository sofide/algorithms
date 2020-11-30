import pytest

from c01_w03_quick_sort import quick_sort, last_pivot


QUICK_SORT_FIRST_PIVOT_CASES = [
    ([2, 1], [1, 2], 1),
    ([2, 1, 3], [1, 2, 3], 2),
    ([5, 1, 6, 4, 2, 3, 7], [1, 2, 3, 4, 5, 6, 7], 16),
]
@pytest.mark.parametrize("array,expected,comparisons", QUICK_SORT_FIRST_PIVOT_CASES)
def test_quick_sort_first_pivot(array, expected, comparisons):
    assert quick_sort(array, last_pivot) == (expected, comparisons)
