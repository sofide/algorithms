import sys

def firtst_pivot(array):
    return 0, array[0]


def last_pivot(array):
    index = len(array) - 1
    return index, array[index]

def median_of_three_pivot(array):
    size = len(array)
    if size % 2 == 0:
        middle_index = (size // 2) - 1
    else:
        middle_index = size // 2

    first = array[0]
    middle = array[middle_index]
    last = array[-1]

    if (first < middle < last) or (first > middle > last):
        return middle_index, middle

    if (first < last < middle) or (first > last > middle):
        last_index = size -1
        return last_index, last

    return 0, first


def print_depth(text, depth):
    # print("-"*4*depth + text)
    pass


def quick_sort(array, pivot_selector=firtst_pivot, depth=0):
    print_depth(f"SORTING ARRAY {array}", depth)
    size = len(array)
    if size <= 1:
        return array, 0

    pivot_index, pivot = pivot_selector(array)

    first_element = array[0]
    array[0] = pivot
    array[pivot_index] = first_element

    separation_index = 1
    print_depth(f"SELECTED PIVOT AT START {array}", depth)

    for inspected_index in range(1, size):
        inspected_value = array[inspected_index]
        if inspected_value < pivot:
            print_depth(f"inspected value {inspected_value} smaller than pivot {pivot}", depth)
            print_depth(f"array {array} - inspected_index {inspected_index} - separation_index {separation_index}", depth)
            first_bigger_value = array[separation_index]
            array[inspected_index] = first_bigger_value
            array[separation_index] = inspected_value
            separation_index += 1
            print_depth(f"array {array} - inspected_index {inspected_index} - separation_index {separation_index}", depth)

    last_lower_value = array[separation_index - 1]

    array[0] = last_lower_value
    array[separation_index -1] = pivot

    left, left_comparisons = quick_sort(array[:separation_index-1], pivot_selector, depth+1)
    right, right_comparisons = quick_sort(array[separation_index:], pivot_selector, depth+1)

    sorted_list = left + [pivot] + right
    comparisons = left_comparisons + right_comparisons + size - 1
    print_depth(f"SORTED ARRAY {sorted_list}", depth)

    return sorted_list, comparisons


def get_list_from_file(filepath):
    with open(filepath) as file:
        raw_numbers = file.readlines()

    return [int(number.strip()) for number in raw_numbers]


if __name__ == "__main__":
    try:
        input_list = [int(x) for x in sys.argv[1:]]

        print(quick_sort(input_list))
    except ValueError:
        file_path = sys.argv[1]
        print(f"Procesing the file {file_path}")

        input_list = get_list_from_file(file_path)
        print(f"Received a list of {len(input_list)} elements")

        _, comparisons = quick_sort(input_list, median_of_three_pivot)
        print(f"comparisons: {comparisons}")
