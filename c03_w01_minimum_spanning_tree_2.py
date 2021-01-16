"""
3.
Pregunta 3
In this programming problem you'll code up Prim's minimum spanning tree algorithm.

Use the file c03_w01_homework_input_2.txt

This file describes an undirected graph with integer edge costs.  It has the format

[number_of_nodes] [number_of_edges]

[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]

[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]

...

For example, the third line of the file is "2 3 -8874", indicating that there is an edge
connecting vertex #2 and vertex #3 that has cost -8874.

You should NOT assume that edge costs are positive, nor should you assume that they are
distinct.

Your task is to run Prim's minimum spanning tree algorithm on this graph.  You should
report the overall cost of a minimum spanning tree --- an integer, which may or may not
be negative --- in the box below.

IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn) time
implementation of Prim's algorithm should work fine. OPTIONAL: For those of you seeking
an additional challenge, try implementing a heap-based version. The simpler approach,
which should already give you a healthy speed-up, is to maintain relevant edges in a
heap (with keys = edge costs).  The superior approach stores the unprocessed vertices in
the heap, as described in lecture.  Note this requires a heap that supports deletions,
and you'll probably need to maintain some kind of mapping between vertices and their
positions in the heap.

CORRECT ANSWER: -3612829
"""
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappush, heappop
from time import time


@dataclass(order=True)
class Edge:
    length: int
    vertices: tuple = field(compare=False)


@dataclass
class MinimumSpanningTree:
    filename: str
    processed_vertices: set = field(default_factory=set)
    crossing_edges: list = field(default_factory=list)
    minimum_spanning_tree: list = field(default_factory=list)

    @property
    def graph(self):
        """
        For a graph with this shape:
        [a]--10--[b]--5--[c]
        |
        +--3--[d]

        it will return a graph with this structure:
        {
            "a": {"b": 10, "d": 3},
            "b": {"c": 5, "a": 10},
            "c": {"b": 5}
            "d": {"a": 3}
        }
        Where each key is a node and its value is a dict with all the edges connected
        to it. For example:
        - node "a" is connected to "b" with a edge of size 10 and to "d" with an edge
        of size 3
        - node "c" is only connected to "a" with the edge mentioned before.
        So:
        {"a": {"b": 10, "d": 3}, "d": {"a": 3}}
        """
        if not hasattr(self, "_graph"):
            self._graph = defaultdict(dict)
            with open(self.filename) as file:
                validation_info, *edges = file.readlines()
                for edge in edges:
                    node_1, node_2, edge_size = edge.split()
                    edge_size = int(edge_size)
                    self._graph[node_1][node_2] = edge_size
                    self._graph[node_2][node_1] = edge_size

                total_vertices, total_edges = validation_info.split()
                total_vertices, total_edges = int(total_vertices), int(total_edges)

                assert len(self.graph) == total_vertices
                assert sum(len(vertex_edges) for vertex_edges in self._graph.values()) == total_edges * 2

        return self._graph

    @property
    def vertices(self):
        if not hasattr(self, "_vertices"):
            self._vertices = set(self.graph.keys())

        return self._vertices

    def calc_minimum_spanning_tree(self):
        for initial_vertex in self.vertices:
            break

        self.process_vertex(vertex=initial_vertex)

        while self.processed_vertices != self.vertices:
            next_vertex = self.get_next_vertex()
            self.process_vertex(next_vertex)


    def process_vertex(self, vertex):
        self.processed_vertices.add(vertex)
        for connected_vertex, edge_length in self.graph[vertex].items():
            if connected_vertex not in self.processed_vertices:
                crossing_edge = Edge(edge_length, (vertex, connected_vertex))
                heappush(self.crossing_edges, crossing_edge)

    def get_next_vertex(self):
        while self.crossing_edges:
            edge = heappop(self.crossing_edges)
            _, next_vertex = edge.vertices
            if next_vertex not in self.processed_vertices:
                self.minimum_spanning_tree.append(edge)
                return next_vertex

        raise IndexError("empty crossing edges")

if __name__ == "__main__":
    starting_time = time()
    filename = sys.argv[1]
    problem = MinimumSpanningTree(filename)

    problem.calc_minimum_spanning_tree()

    # print(problem.graph)
    print("Minimum spanning tree:")
    # print(problem.minimum_spanning_tree)

    print("Minimum Spanning Tree cost:")
    print(sum(edge.length for edge in problem.minimum_spanning_tree))

    # print(f"shortest path: {problem.shortest_path}")

    end_time = time()

    print(f"Running time: {end_time - starting_time}")
