"""
In this assignment you will implement one or more algorithms for the all-pairs
shortest-path problem.  Here are data files describing three graphs:

c04_w01_homework_input_1.txt
c04_w01_homework_input_2.txt
c04_w01_homework_input_3.txt

The first line indicates the number of vertices and edges, respectively.  Each
subsequent line describes an edge (the first two numbers are its tail and head,
respectively) and its length (the third number).  NOTE: some of the edge lengths are
negative.  NOTE: These graphs may or may not have negative-cost cycles.

Your task is to compute the "shortest shortest path".  Precisely, you must first
identify which, if any, of the three graphs have no negative cycles.  For each such
graph, you should compute all-pairs shortest paths and remember the smallest one
(i.e., compute min_{u,v in V} d(u,v) where d(u,v) denotes the shortest-path distance
from u to v).

If each of the three graphs has a negative-cost cycle, then enter "NULL" in the box
below.  If exactly one graph has no negative-cost cycles, then enter the length of its
shortest shortest path in the box below.  If two or more of the graphs have no
negative-cost cycles, then enter the smallest of the lengths of their shortest shortest
paths in the box below.

OPTIONAL: You can use whatever algorithm you like to solve this question. If you have
extra time, try comparing the performance of different all-pairs shortest-path
algorithms!

OPTIONAL: Here is a bigger data set to play with.

c04_w01_homework_input_4_large.txt

For fun, try computing the shortest shortest path of the graph in the file above.
"""
from collections import defaultdict
import sys

import numpy
from tqdm import tqdm

class NegativeCycleError(Exception):
    pass


class AllPairsShortestPath:
    def __init__(self, filename):
        self.graph = defaultdict(dict)
        # the graph is a dict with the following structure:
        # {1: {2: cost_1_2, 3: cost_1_3}, ... }
        with open(filename) as graphfile:
            data, *edges = graphfile.readlines()

        self.total_vertices, self.total_edges = map(int, data.split())

        assert len(edges) == self.total_edges

        for edge_info in edges:
            tail, head, length = map(int, edge_info.split())

            tail -= 1
            head -= 1

            self.graph[tail][head] = length

        assert len(self.graph) == self.total_vertices


class FloydWarshallAlgorithm(AllPairsShortestPath):
    def solve(self):
        calc_shape = (self.total_vertices, self.total_vertices)
        previous_calc = numpy.ones(calc_shape)
        previous_calc *= numpy.inf

        # Base cases
        for tail, edges in self.graph.items():
            previous_calc[tail][tail] = 0
            for head, length in edges.items():
                previous_calc[tail][head] = length

        # Main loop
        for vertex_k in tqdm(self.graph):
            # Analyze one vertex (vertex_k) per loop
            current_calc = numpy.zeros(calc_shape)
            for tail in self.graph:
                for head in self.graph:
                    # check if vertex_k should be included in the shortest path
                    current_calc[tail][head] = min(
                        previous_calc[tail][head],
                        previous_calc[tail][vertex_k] + previous_calc[vertex_k][head],
                    )

                    if tail == head and current_calc[tail][head] < 0:
                        raise NegativeCycleError

            previous_calc = current_calc

        return current_calc.min()


if __name__ == "__main__":
    filename = sys.argv[1]

    problem = FloydWarshallAlgorithm(filename)

    try:
        print(f"✅ {problem.solve()}")

    except NegativeCycleError:
        print("❌ negative cycle!")
