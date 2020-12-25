import sys
from dataclasses import dataclass
from time import time

NO_PATH_LENGHT = 1000000


@dataclass
class DijkstraShortestPath:
    filename: str
    processed_vertices = set()
    shortest_path = {}

    @property
    def graph(self):
        if not hasattr(self, "_graph"):
            self._graph = {}
            with open(self.filename) as file:
                for line in file.readlines():
                    tail, *edges = line.split()
                    edges = [edge.split(",") for edge in edges]
                    self._graph[tail] = {head: int(length) for head, length in edges}

        return self._graph

    @property
    def vertices(self):
        if not hasattr(self, "_vertices"):
            self._vertices = set(self.graph.keys())

        return self._vertices

    def calc_shortest_path(self, start="1"):
        self.shortest_path[start] = 0
        self.processed_vertices.add(start)

        while self.processed_vertices != self.vertices:
            crossing_edges = [
                (tail, head, self.shortest_path[tail] + self.graph[tail][head])
                for tail in self.processed_vertices
                for head in self.graph[tail] if head not in self.processed_vertices
            ]
            _, vertex, path_lenght = min(crossing_edges, key= lambda x: x[-1])
            self.shortest_path[vertex] = path_lenght
            self.processed_vertices.add(vertex)


if __name__ == "__main__":
    starting_time = time()
    filename = sys.argv[1]
    problem = DijkstraShortestPath(filename)

    # print(problem.graph)
    problem.calc_shortest_path()

    # print(f"shortest path: {problem.shortest_path}")

    print("solution:")
    nodes_to_report = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    print(",".join(str(problem.shortest_path[str(vertex)]) for vertex in nodes_to_report))
    end_time = time()

    print(f"Running time: {end_time - starting_time}")
