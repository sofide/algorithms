"""
In this assignment you will implement one or more algorithms for the 2SAT problem.  Here
are 6 different 2SAT instances:

- c04_w04_homework_input_1.txt
- c04_w04_homework_input_2.txt
- c04_w04_homework_input_3.txt
- c04_w04_homework_input_4.txt
- c04_w04_homework_input_5.txt
- c04_w04_homework_input_6.txt

The file format is as follows.  In each instance, the number of variables and the number
of clauses is the same, and this number is specified on the first line of the file.
Each subsequent line specifies a clause via its two literals, with a number denoting the
variable and a "-" sign denoting logical "not".  For example, the second line of the
first data file is "-16808 75250", which indicates the clause ¬x16808 ∨ x75250.

Your task is to determine which of the 6 instances are satisfiable, and which are
unsatisfiable.  In the box below, enter a 6-bit string, where the ith bit should be 1 if
the ith instance is satisfiable, and 0 otherwise.  For example, if you think that the
first 3 instances are satisfiable and the last 3 are not, then you should enter the
string 111000 in the box below.

DISCUSSION: This assignment is deliberately open-ended, and you can implement whichever
2SAT algorithm you want.  For example, 2SAT reduces to computing the strongly connected
components of a suitable graph (with two vertices per variable and two directed edges
per clause, you should think through the details).  This might be an especially
attractive option for those of you who coded up an SCC algorithm in Part 2 of this
specialization.  Alternatively, you can use Papadimitriou's randomized local search
algorithm.  (The algorithm from lecture is probably too slow as stated, so you might
want to make one or more simple modifications to it --- even if this means breaking the
analysis given in lecture --- to ensure that it runs in a reasonable amount of time.)
A third approach is via backtracking. In lecture we mentioned this approach only in
passing; see Chapter 9 of the Dasgupta-Papadimitriou-Vazirani book, for example, for
more details.
"""
from collections import defaultdict
from dataclasses import dataclass, field
import math
import random
import sys

from tqdm import tqdm


def get_clauses_from_file(filename):
    with open(filename) as clauses_file:
        total_clauses, *clauses = clauses_file.readlines()

    clauses = [tuple(map(int, clause.split())) for clause in clauses]

    assert len(clauses) == int(total_clauses)

    return clauses


@dataclass
class Variable:
    value: bool = field(default_factory=lambda: random.choice((True, False)))
    clauses_indexes: list = field(default_factory=list)


class PapadimitriouAlgorithm:
    def __init__(self, clauses: list[tuple]):
        self.clauses = clauses
        self.assignments = None
        self.invalid_clauses = None

    def clause_is_valid(self, clause):
        """
        Return True if the cluse is valid with the current assignments, or False
        otherwise.

        For example:
        the clause (1, 2) is interpreted as "x1 or x2", so this method will return
        True if:
            - assignments[1] and assignments[2] are True
            - assignments[1] is True and assignments[2] is False
            - assignments[1] is False and assignments[2] is True
        False if:
            - assignments[1] and assignments[2] are False

        If a variable is negative is interpreted as "not". So the clause (1, -2) is
        interpreted as "x1 or not x2"
        """
        part_one, part_two = clause


        expected_part_one_value = part_one > 0
        part_one_value = self.assignments[abs(part_one)].value
        part_one_has_expected_value = part_one_value == expected_part_one_value

        expected_part_two_value = part_two > 0
        part_two_value = self.assignments[abs(part_two)].value
        part_two_has_expected_value = part_two_value == expected_part_two_value

        return part_one_has_expected_value or part_two_has_expected_value


    def random_initialization(self):
        # first time random initialization create assignments dict
        if self.assignments is None:
            self.assignments = defaultdict(Variable)
            self.invalid_clauses = set()
            for index, (var_1, var_2) in enumerate(self.clauses):
                self.assignments[abs(var_1)].clauses_indexes.append(index)
                self.assignments[abs(var_2)].clauses_indexes.append(index)

                if not self.clause_is_valid((var_1, var_2)):
                    self.invalid_clauses.add(index)

            self.assignments = dict(self.assignments)

        else:
            for variable in self.assignments.values():
                variable.value = random.choice((True, False))

            self.invalid_clauses = set(
                index
                for index, clause in enumerate(self.clauses)
                if not self.clause_is_valid(clause)
            )

    def switch_variable(self, variable_name):
        """
        Switch variable value and recalc invalid_clauses.
        """
        variable = self.assignments[variable_name]

        # if variable has value in False switch it to True, and if it has value in True
        # switch it to False
        variable.value = variable.value == False

        for clause_index in variable.clauses_indexes:
            if self.clause_is_valid(self.clauses[clause_index]):
                self.invalid_clauses.discard(clause_index)

            else:
                self.invalid_clauses.add(clause_index)

    def print_status(self):
        for variable_name, variable in self.assignments.items():
            print(f"{variable_name} = {variable.value}")

        for clause in self.clauses:
            part_one, part_two = clause
            part_one_value = self.assignments[abs(part_one)].value
            part_two_value = self.assignments[abs(part_two)].value
            valid = self.clause_is_valid(clause)
            print(f"{clause} | {part_one} = {part_one_value} | {part_two} = {part_two_value} | valid clause = {valid}")

    def solve(self, debug=False):
        total_clauses = len(self.clauses)
        outer_iterations = int(math.log2(total_clauses))
        inner_iterations = 2 * (total_clauses ** 2)
        inner_pbar_ratio = 1000

        for _ in tqdm(range(outer_iterations), desc="outer_loop"):
            self.random_initialization()

            inner_progress_bar = tqdm(total=inner_iterations, desc="inner_loop")
            for inner_it in range(inner_iterations):
                if inner_it and inner_it % inner_pbar_ratio == 0:
                    inner_progress_bar.update(inner_pbar_ratio)

                if debug:
                    self.print_status()
                if not self.invalid_clauses:
                    return True

                random_clause = random.choice(list(self.invalid_clauses))
                random_variable = abs(random.choice(self.clauses[random_clause]))
                self.switch_variable(random_variable)
                if debug:
                    print(f"random variable to switch = {random_variable}")
                    input()

        return False


if __name__ == "__main__":
    filename = sys.argv[1]

    if filename == "test":
        testing_input = [
            (1, 2),
            (-1, 3),
            (3, 4),
            (-2, -4),
        ]
        # should be True with assignations:
        # x1 = x3 = True
        # x2 = x4 = False
        problem = PapadimitriouAlgorithm(testing_input)
        print(problem.solve(debug=True))
        print(problem.assignments)

        sys.exit()

    clauses = get_clauses_from_file(filename)

    problem = PapadimitriouAlgorithm(clauses)
    print(problem.solve())
