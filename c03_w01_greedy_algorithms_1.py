"""
1. In this programming problem and the next you'll code up the greedy algorithms from
lecture for minimizing the weighted sum of completion times..

Use the file c03_w01_homework_input_1.txt

This file describes a set of jobs with positive and integral weights and lengths.  It
has the format:

[number_of_jobs]
[job_1_weight] [job_1_length]
[job_2_weight] [job_2_length]
...

For example, the third line of the file is "74 59", indicating that the second job has
weight 74 and length 59.

You should NOT assume that edge weights or lengths are distinct.

Your task in this problem is to run the greedy algorithm that schedules jobs in
decreasing order of the difference (weight - length).  Recall from lecture that this
algorithm is not always optimal.  IMPORTANT: if two jobs have equal difference (weight
- length), you should schedule the job with higher weight first.  Beware: if you break
ties in a different way, you are likely to get the wrong answer.  You should report the
sum of weighted completion times of the resulting schedule --- a positive integer --- in
the box below.

ADVICE: If you get the wrong answer, try out some small test cases to debug your
algorithm (and post your test cases to the discussion forum).

-------
2. For this problem, use the same data set as in the previous problem.

Your task now is to run the greedy algorithm that schedules jobs (optimally) in
decreasing order of the ratio (weight/length).  In this algorithm, it does not matter
how you break ties.  You should report the sum of weighted completion times of the
resulting schedule --- a positive integer --- in the box below.
"""
import sys
from dataclasses import dataclass
from typing import Callable


@dataclass(order=True)
class WeightedTask:
    greedy_calc: int
    weight: int
    length: int


@dataclass
class GreedyProblem:
    filename: str
    greedy_calc: Callable[[int, int], int]

    @property
    def ordered_tasks(self):
        if not hasattr(self, "_ordered_tasks"):
            with open(self.filename) as file:
                quantity, *raw_tasks = file.readlines()

            quantity = int(quantity)
            self._ordered_tasks = []

            for task in raw_tasks:
                weight, length = task.split()
                weight, length = int(weight), int(length)
                self._ordered_tasks.append(
                    WeightedTask(self.greedy_calc(weight, length), weight, length)
                )

            self._ordered_tasks.sort(reverse=True)

            assert len(self._ordered_tasks) == quantity

        return self._ordered_tasks


    def weighted_completion_time(self):
        accumulated_time = 0
        completion = 0

        for task in self.ordered_tasks:
            accumulated_time += task.length
            completion += accumulated_time * task.weight

        return completion


def greedy_difference(weight, length):
    return weight - length


def greedy_ratio(weight, length):
    return weight / length


if __name__ == "__main__":
    filename = sys.argv[1]

    problem_difference = GreedyProblem(filename, greedy_difference)
    print("WEIGHTED COMPLETION TIME DIFFERENCE")
    print(problem_difference.ordered_tasks)
    print(problem_difference.weighted_completion_time())

    problem_ratio = GreedyProblem(filename, greedy_ratio)
    print("WEIGHTED COMPLETION TIME RATIO")
    print(problem_ratio.ordered_tasks)
    print(problem_ratio.weighted_completion_time())
