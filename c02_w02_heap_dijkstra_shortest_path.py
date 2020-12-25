import sys
from dataclasses import dataclass, field
from heapq import heappush, heappop
from time import time


NO_PATH_LENGHT = 1000000


@dataclass(order=True)
class CrossingEdge:
    path_lenght: int
    tail: str = field(compare=False)
    head: str = field(compare=False)


@dataclass
class DijkstraShortestPath:
    filename: str
    processed_vertices: set = field(default_factory=set)
    shortest_path: dict = field(default_factory=dict)
    crossing_edges: list = field(default_factory=list)

    @property
    def graph(self):
        """
        For a graph with this shape:
        [a] --10--> [b] --5--> [c]
        |
        + --3--> [d]

        it will return a graph with this structure:
        {
            "a": {"b": 10, "d": 3},
            "b": {"c": 5},
        }
        Where the keys of the outer dict are tails, and the keys and values of the inner
        dict are the heads and edge length respectively.
        """
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
        self.process_vertex(vertex=start, v_shortest_path=0)

        while self.processed_vertices != self.vertices:
            next_edge = self.get_next_edge()
            self.process_vertex(
                vertex=next_edge.head, v_shortest_path=next_edge.path_lenght
            )

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
