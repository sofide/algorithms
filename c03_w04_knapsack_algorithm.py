"""
1. In this programming problem and the next you'll code up the knapsack algorithm from
lecture.

Let's start with a warm-up.

Use the file c03_w04_homework_input_1.txt

This file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
...

For example, the third line of the file is "50074 659", indicating that the second item
has value 50074 and size 659, respectively.

You can assume that all numbers are positive. You should assume that item weights and
the knapsack capacity are integers.

In the box below, type in the value of the optimal solution.

ADVICE: If you're not getting the correct answer, try debugging your algorithm using
some small test cases. And then post them to the discussion forum!

Correct answer: 2493893

---------
2. This problem also asks you to solve a knapsack instance, but a much bigger one.

Use the file c03_w04_homework_input_2.txt

This file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
...

For example, the third line of the file is "50074 834558", indicating that the second
item has value 50074 and size 834558, respectively.  As before, you should assume
that item weights and the knapsack capacity are integers.

This instance is so big that the straightforward iterative implemetation uses an
infeasible amount of time and space.  So you will have to be creative to compute an
optimal solution.  One idea is to go back to a recursive implementation, solving
subproblems --- and, of course, caching the results to avoid redundant work --- only on
an "as needed" basis.  Also, be sure to think about appropriate data structures for
storing and looking up solutions to subproblems.

In the box below, type in the value of the optimal solution.

ADVICE: If you're not getting the correct answer, try debugging your algorithm using
some small test cases. And then post them to the discussion forum!

correct answer: 4243395
"""
import sys
from collections import defaultdict

import numpy
from tqdm import tqdm


class KnapsackProblem:
    def __init__(self, filename):
        with open(filename) as problem_input:
            problem_info, *items = problem_input.readlines()

        knapsack_size, number_of_items = problem_info.split()

        self.knapsack_size = int(knapsack_size)
        self.number_of_items = int(number_of_items)

        self.items = [
            (int(value), int(weight))
            for value, weight
            in (item_line.split() for item_line in items)
        ]
        assert (len(self.items)) == self.number_of_items

    def solve(self):
        partial_result = numpy.zeros((self.number_of_items + 1, self.knapsack_size + 1))

        for index, item in tqdm(enumerate(self.items, 1), total=self.number_of_items):
            item_value, item_weight = item

            for partial_weight in range(self.knapsack_size + 1):
                if item_weight > partial_weight:
                    including_current_item = 0
                else:
                    before_including = partial_result[index - 1][partial_weight - item_weight]
                    including_current_item = before_including + item_value

                no_including = partial_result[index - 1][partial_weight]

                partial_result[index][partial_weight] = max(including_current_item, no_including)

        self.partial_result_matrix = partial_result

        return partial_result[self.number_of_items][self.knapsack_size]


class KnapsackProblemBig(KnapsackProblem):
    def _partial_solution(self, previous_colum, size, item_weight, item_value):
        with_new_item = previous_colum[size - item_weight] + item_value
        without_new_item = previous_colum[size]

        return max(with_new_item, without_new_item)

    def solve(self):
        previous_colum = [0] * (self.knapsack_size + 1)

        for item_value, item_weight in tqdm(self.items):
            if item_weight > self.knapsack_size:
                # dont try to carry an item bigger than the capacity of the knapsack
                continue

            value_max_capacity = self._partial_solution(
                previous_colum, self.knapsack_size, item_weight, item_value
            )

            # avoid inserting current item in capasities lower than current_item
            current_column = previous_colum[:item_weight]
            for partial_weight in range(item_weight, self.knapsack_size + 1):
                value_current_capacity = self._partial_solution(
                    previous_colum, partial_weight, item_weight, item_value
                )
                if value_current_capacity == value_max_capacity:
                    pending_calcs = self.knapsack_size - partial_weight + 1
                    current_column.extend([value_max_capacity] * pending_calcs)
                    break

                current_column.append(value_current_capacity)

            previous_colum = current_column

        return current_column[self.knapsack_size]

class KnapsackProblemBigSecond(KnapsackProblemBig):
    def solve(self):
        items_with_info = []
        for item_value, item_weight in reversed(self.items):
            if not items_with_info:
                sizes_to_calc = {self.knapsack_size: 0}
                items_with_info.insert(0, (item_value, item_weight, sizes_to_calc))
                continue

            _, next_item_weight, next_item_sizes_to_calc = items_with_info[0]
            sizes_to_calc = {}
            for size_next in next_item_sizes_to_calc:
                # for calculation without including next element
                sizes_to_calc[size_next] = 0
                # for calculation including next element
                if next_item_weight <= size_next:
                    sizes_to_calc[size_next - next_item_weight] = 0

            items_with_info.insert(0, (item_value, item_weight, sizes_to_calc))

        # dummy previous item for first iteration
        previous_item_sizes = defaultdict(int)

        for item_value, item_weight, sizes_to_calc in tqdm(items_with_info):
            for size in sizes_to_calc:
                if item_weight > size:
                    sizes_to_calc[size] = previous_item_sizes[size]
                    continue
                include_element = previous_item_sizes[size - item_weight] + item_value
                exclude_element = previous_item_sizes[size]

                sizes_to_calc[size] = max(include_element, exclude_element)

            previous_item_sizes = sizes_to_calc

        return items_with_info[-1][-1][self.knapsack_size]


if __name__ == "__main__":
    filename = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[2].lower() == "big":
            problem = KnapsackProblemBig(filename)
        else:
            problem = KnapsackProblemBigSecond(filename)
    else:
        problem = KnapsackProblem(filename)

    # with testing file c03_w04_testing_input_1.txt expected result = 8
    print(problem.solve())
