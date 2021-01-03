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
"""
import sys

from tqdm import tqdm

class MyHashTable:
    def __init__(self, n_buckets: int = 10_000_000):
        self.n_buckets = n_buckets
        self.buckets = [set() for x in range(self.n_buckets)]

    def hash_func(self, number):
        return abs(number) % self.n_buckets

    def insert(self, number):
        position = self.hash_func(number)
        self.buckets[position].add(number)

    def lookup(self, number):
        # position = self.hash_func(number)
        position = abs(number) % self.n_buckets
        return number in self.buckets[position]

class Sum2Problem:
    def __init__(self, filename):
        self.numbers = set()
        self.hash_table = MyHashTable()

        with open(filename) as f:
            for number in f.readlines():
                number = int(number)
                self.numbers.add(number)
                self.hash_table.insert(number)

        print(f"size of numbers: {len(self.numbers)}")
        print(f"number of buckets: {self.hash_table.n_buckets}")

    def sum_2(self, target):
        """
        return True if there is any distinct x and y in self.numbers such as:
        x + y = target
        """
        for x in self.numbers:
            y = target - x
            if x != y and self.hash_table.lookup(y):
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
