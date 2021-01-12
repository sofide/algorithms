"""
The goal of this problem is to implement a variant of the 2-SUM algorithm covered in
this week's lectures.

The file contains 1 million integers, both positive and negative (there might be some
repetitions!).This is your array of integers, with the i^th row of the file specifying
the i^ th entry of the array.

Your task is to compute the number of target values tt in the interval [-10000,10000]
(inclusive) such that there are distinct numbers x,yx,y in the input file that satisfy
x+y=t. (NOTE: ensuring distinctness requires a one-line addition to the algorithm from
lecture.)

Write your numeric answer (an integer between 0 and 20001) in the space provided.

OPTIONAL CHALLENGE: If this problem is too easy for you, try implementing your own hash
table for it. For example, you could compare performance under the chaining and open
addressing approaches to resolving collisions.

CORRECT ANSWER: 427
"""
import sys
from dataclasses import dataclass

from tqdm import tqdm


class Sum2Problem:
    def __init__(self, filename):
        with open(filename) as f:
            self.numbers = {int(number) for number in f.readlines()}
        print(f"size of numbers set: {len(self.numbers)}")
        self.sorted_numbers = sorted(self.numbers)

    def sum_2(self, target):
        """
        return True if there is any distinct x and y in self.numbers such as:
        x + y = target
        """
        half_target = round(target / 2)

        for x in self.sorted_numbers:
            if x >= half_target:
                break
            y = target - x
            if x != y and y in self.numbers:
                return True

        return False

if __name__ == "__main__":
    filename = sys.argv[1]
    print(f"loading file '{filename}'")

    problem = Sum2Problem(filename)

    sum_2_count = 0

    progress_bar = tqdm(range(-10000, 10000))
    progress_bar.set_description(f"Count so far {sum_2_count}")
    for target in progress_bar:
        if problem.sum_2(target):
            sum_2_count += 1
            progress_bar.set_description(f"Count so far {sum_2_count}")

    print(f"total sum_2_count = {sum_2_count}")
