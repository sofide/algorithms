import random


def random_pivot(array):
    index = random.choice(range(len(array)))
    value = array[index]

    return index, value


def rselect(array, ith_smallest, pivot_selector=random_pivot):
    """
    Get the i^th smallest element from an unordered list.

    For example:
        - for a list = [1, 143, 42, 23, 4]
        - and for a ith_smallest = 2
    the returned value is 4
    """
    pivot_i, pivot_value = pivot_selector(array)

    # move the pivot to the first position
    first_value = array[0]
    array[0] = pivot_value
    array[pivot_i] = first_value

    # separation between the items smaller than pivot and greater ones
    separation_index = 1

    for inspected_index in range(1, len(array)):
        inspected_value = array[inspected_index]
        if inspected_value < pivot_value:
            first_bigger = array[separation_index]
            array[separation_index] = inspected_value
            array[inspected_index] = first_bigger

            separation_index += 1

    if ith_smallest == separation_index:
        return pivot_value

    elif ith_smallest < separation_index:
        # the ith_smallest is on the left of the pivot
        return rselect(array[1:separation_index], ith_smallest)

    else:
        # the ith_smallest is on the right of the  pivot
        return rselect(array[separation_index:], ith_smallest - separation_index)
