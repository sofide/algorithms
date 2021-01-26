"""
Pregunta 3
In this programming problem you'll code up the dynamic programming algorithm for
computing a maximum-weight independent set of a path graph.

Use the file c03_w03_homework_input_3.txt

This file describes the weights of the vertices in a path graph (with the weights listed
in the order in which vertices appear in the path). It has the following format:

[number_of_vertices]
[weight of first vertex]
[weight of second vertex]
...

For example, the third line of the file is "6395702," indicating that the weight of the
second vertex of the graph is 6395702.

Your task in this problem is to run the dynamic programming algorithm (and the
reconstruction procedure) from lecture on this data set.  The question is: of the
vertices 1, 2, 3, 4, 17, 117, 517, and 997, which ones belong to the maximum-weight
independent set?  (By "vertex 1" we mean the first vertex of the graph---there is no
vertex 0.)   In the box below, enter a 8-bit string, where the ith bit should be 1 if
the ith of these 8 vertices is in the maximum-weight independent set, and 0 otherwise.
For example, if you think that the vertices 1, 4, 17, and 517 are in the maximum-weight
independent set and the other four vertices are not, then you should enter the string
10011010 in the box below.
"""
import sys


class MaxWeightIndependentSet:
    def __init__(self, filename: str):
        with open(filename) as path_file:
            total_vertices, *vertices_weight = path_file.readlines()

        self.path_graph = [int(weight) for weight in vertices_weight]

        self.total_vertices = int(total_vertices)

        assert len(self.path_graph) == self.total_vertices

    def max_wis_weight_calc(self):
        self.partial_wis_weight = []

        for index, vertex_weight in enumerate(self.path_graph):
            if index == 0:
                # For a path with only one element select that element
                self.partial_wis_weight.append(vertex_weight)
                continue

            if index == 1:
                # For a path with only two elements select the bigger one
                self.partial_wis_weight.append(max(self.path_graph[:2]))
                continue

            # For paths with more than two elements select the best WIS by including
            # or excluding the last element
            excluding_current_vertex = self.partial_wis_weight[index-1]
            including_current_vertex = self.partial_wis_weight[index-2] + vertex_weight

            self.partial_wis_weight.append(max(
                (excluding_current_vertex, including_current_vertex)
            ))

        assert len(self.partial_wis_weight) == self.total_vertices

        return self.partial_wis_weight


    def reconstruction_algorithm(self):
        self.max_wis_vertices = set()

        index = self.total_vertices - 1

        while index >= 1:
            wis_including_current = self.partial_wis_weight[index]
            wis_excluding_current = self.partial_wis_weight[index - 1]

            if wis_excluding_current >= wis_including_current:
                index -= 1
            else:
                self.max_wis_vertices.add(index)
                index -= 2

        if index == 0:
            self.max_wis_vertices.add(index)

        return self.max_wis_vertices


    def check_if_in_max_wis(self, vertices=(1, 2, 3, 4, 17, 117, 517, 997)):
        # max_wis_vertices indexes start in 0 but in homework the vertex 1 is
        # the first one
        solution = ""
        for vertex in vertices:
            if vertex - 1 in self.max_wis_vertices:
                solution += "1"
            else:
                solution += "0"

        return solution


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        filename = "c03_w03_testing_input_3.txt"
        vertices_to_check = [1, 2, 3, 4, 5, 6]

    else:
        filename = "c03_w03_homework_input_3.txt"
        vertices_to_check = [1, 2, 3, 4, 17, 117, 517, 997]

    problem = MaxWeightIndependentSet(filename)
    problem.max_wis_weight_calc()
    problem.reconstruction_algorithm()
    print(problem.check_if_in_max_wis(vertices_to_check))
