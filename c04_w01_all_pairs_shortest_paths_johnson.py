from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappush, heappop
import sys

import numpy
from tqdm import tqdm

from c04_w01_all_pairs_shortest_paths import AllPairsShortestPath, NegativeCycleError


@dataclass
class BellmanFord:
    graph: dict
    source: int

    def solve(self):
        inverted_graph = defaultdict(dict)
        for tail, edge in self.graph.items():
            for head, length in edge.items():
                inverted_graph[head][tail] = length

        previous_calc = {
            vertex: numpy.inf
            for vertex in self.graph
        }
        previous_calc[self.source] = 0

        total_vertices = len(self.graph)
        max_edges_in_path = total_vertices - 1

        # run one extra iteration to detect negative cycles
        total_iterations = max_edges_in_path + 1
        last_iteration_index = total_iterations - 1

        for max_edges in range(total_iterations):
            current_calc = {}
            for vertex in self.graph:
                if vertex == self.source:
                    current_calc[self.source] = 0
                    continue
                current_calc[vertex] = min(
                    previous_calc[vertex],
                    min(
                        (previous_calc[tail] + length)
                        for tail, length in inverted_graph[vertex].items()

                    )
                )
            if current_calc == previous_calc:
                return current_calc

            if max_edges == last_iteration_index:
                raise NegativeCycleError

            previous_calc = current_calc



@dataclass(order=True)
class CrossingEdge:
    path_lenght: int
    tail: str = field(compare=False)
    head: str = field(compare=False)


@dataclass
class DijkstraShortestPath:
    graph: dict
    source: int

    def calc_shortest_path(self):
        self.shortest_path = {}
        self.processed_vertices = set()
        self.crossing_edges = []
        vertices = set(self.graph)

        self.process_vertex(vertex=self.source, v_shortest_path=0)

        while self.processed_vertices != vertices:
            next_edge = self.get_next_edge()
            self.process_vertex(
                vertex=next_edge.head, v_shortest_path=next_edge.path_lenght
            )

        return self.shortest_path

    def process_vertex(self, vertex, v_shortest_path):
        self.shortest_path[vertex] = v_shortest_path
        self.processed_vertices.add(vertex)
        for head, edge_lenght in self.graph[vertex].items():
            if head not in self.processed_vertices:
                path_lenght = v_shortest_path + edge_lenght
                crossing_edge = CrossingEdge(path_lenght, tail=vertex, head=head)
                heappush(self.crossing_edges, crossing_edge)

    def get_next_edge(self):
        while self.crossing_edges:
            edge = heappop(self.crossing_edges)
            if edge.head not in self.processed_vertices:
                return edge

        raise IndexError("empty crossing edges")


class JohnsonAlgorithm(AllPairsShortestPath):
    def solve(self):
        self.graph["source"] = {
            vertex: 0
            for vertex in self.graph
        }

        bellman_ford = BellmanFord(self.graph, "source")
        vertices_values = bellman_ford.solve()

        # transform into nonnegative edges
        self.graph.pop("source")
        self.graph = {
            tail: {
                head: length + vertices_values[tail] - vertices_values[head]
                for head, length in edges.items()
            }
            for tail, edges in self.graph.items()
        }

        current_shortest_path = numpy.inf

        for source_vertex in tqdm(self.graph):
            dijkstra = DijkstraShortestPath(self.graph, source_vertex)
            real_paths_lenghts = {
                head: (length - vertices_values[source_vertex] + vertices_values[head])
                for head, length in dijkstra.calc_shortest_path().items()
            }

            minimum_vertex_path = min(real_paths_lenghts.values())

            if minimum_vertex_path < current_shortest_path:
                current_shortest_path = minimum_vertex_path

        return current_shortest_path


if __name__ == "__main__":
    filename = sys.argv[1]

    problem = JohnsonAlgorithm(filename)

    try:
        print(f"✅ {problem.solve()}")

    except NegativeCycleError:
        print("❌ negative cycle!")
