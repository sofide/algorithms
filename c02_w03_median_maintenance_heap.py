"""
The goal of this problem is to implement the "Median Maintenance" algorithm (covered in
the Week 3 lecture on heap applications).  The text file contains a list of the integers
from 1 to 10000 in unsorted order; you should treat this as a stream of numbers,
arriving one by one.  Letting x_i denote the i-th number of the file, the k-th median
m_k is defined as the median of the numbers x_1,...,x_k.  (So, if k is odd, then m_k is
((k+1)/2)th smallest number among x_1,...,x_k; if k is even, then m_k is the
(k/2)th smallest number among x_1,...,x_k).

In the box below you should type the sum of these 10000 medians, modulo 10000 (i.e.,
only the last 4 digits).  That is, you should compute
(m_1 + m_2 + m_3 + ... + m_10000) mod 10000.

OPTIONAL EXERCISE: Compare the performance achieved by heap-based and search-tree-based
implementations of the algorithm.
"""
import sys
from heapq import heappop, heappush

min_heappush, min_heappop = heappush, heappop

def max_heappush(input_list, element):
    heappush(input_list, - element)


def max_heappop(input_list):
    return - heappop(input_list)


def max_heapget(input_list):
    return - input_list[0]


def median_maintenance(input_list: list):
    heap_low = []
    heap_high = []

    median_so_far = None
    all_intermediate_medians = []

    for element in input_list:
        # initialize median_so_far if it's the first iteration
        if median_so_far is None:
            median_so_far = element

        # insert the element in the low or high list according to its value
        if element <= median_so_far:
            max_heappush(heap_low, element)
        else:
            min_heappush(heap_high, element)

        # balance the low and high lists so they have half items each
        if len(heap_high) > len(heap_low):
            median_top = min_heappop(heap_high)
            max_heappush(heap_low, median_top)
        elif (len(heap_low) - len(heap_high)) > 1:
            # It's ok if heap_low has one element more than heap_high
            # it happens in every odd iteration
            median_bottom = max_heappop(heap_low)
            min_heappush(heap_high, median_bottom)

        median_so_far = max_heapget(heap_low)
        all_intermediate_medians.append(median_so_far)

    return all_intermediate_medians


def get_input_from_file(filename: str):
    with open(filename) as file:
        input_list = [int(number) for number in file.readlines()]

    return input_list


def solve_homework(input_list):
    medians = median_maintenance(input_list)

    medians_sum = sum(medians)

    return medians_sum % 10000


if __name__ == "__main__":
    input_file = sys.argv[1]

    print(f"Reading file {input_file}...")
    input_list = get_input_from_file(input_file)

    print("solving homework...")
    result = solve_homework(input_list)

    print(f"Result: {result}")


