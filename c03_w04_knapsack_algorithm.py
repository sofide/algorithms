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
"""
import sys

import numpy


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

        for index, item in enumerate(self.items, 1):
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




if __name__ == "__main__":
    filename = sys.argv[1]
    problem = KnapsackProblem(filename)

    # with testing file c03_w04_testing_input_1.txt expected result = 8
    print(problem.solve())








