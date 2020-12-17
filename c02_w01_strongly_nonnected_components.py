from collections import defaultdict, Counter
from dataclasses import dataclass
import sys


@dataclass
class StronglyConnectedComponents:
    filename: str

    @property
    def graph(self):
        if not hasattr(self, "_graph"):
            self._graph = defaultdict(list)

            with open(self.filename) as f:
                for edge in f.readlines():
                    tail, head = edge.split()
                    self._graph[tail].append(head)

        return self._graph

    @property
    def inverted_graph(self):
        if not hasattr(self, "_inverted_graph"):
            self._inverted_graph = defaultdict(list)

            for tail, heads in self.graph.items():
                for head in heads:
                    self._inverted_graph[head] = tail

        return self._inverted_graph


    @staticmethod
    def _scc_calc(graph, order=None):
        explored_vertices = []
        finishing_order = []
        components_leaders = Counter()

        def depth_first_search(graph, start, current_leader=None):
            if current_leader is None:
                current_leader = start

            components_leaders[current_leader] += 1
            explored_vertices.append(start)

            for edge_head in graph[start]:
                if edge_head not in explored_vertices:
                    depth_first_search(graph, edge_head, current_leader)

            # print(f"append {start} {len(finishing_order)=}")
            finishing_order.append(start)

        if not order:
            order = list(graph)

        # print(f"the order is: {order=} {len(order)=}")

        for node in order:
            if node not in explored_vertices:
                depth_first_search(graph, node)

        # print(f"finishing order is: {finishing_order=} {len(finishing_order)=}")
        return finishing_order, components_leaders

    def calc(self):
        """
        Compute all the strongly connected components (sccs) and return its leaders and
        size
        """
        finishing_order, _ = self._scc_calc(self.inverted_graph)

        finishing_order.reverse()

        _, components_leaders = self._scc_calc(self.graph, finishing_order)

        return components_leaders


if __name__ == "__main__":
    filename = sys.argv[1]

    print(f"Calculate StronglyConnectedComponents from file {filename}")
    sccs_problem = StronglyConnectedComponents(filename)

    components = sccs_problem.calc()

    how_many = 5
    print(f"Components: {components}")
    print("The {how_many} most bigger:")
    biggers = components.most_common(how_many)

    biggers_size = [str(size) for leader, size in biggers]

    biggers_size += ["0"] * (how_many - len(biggers))

    print(",".join(biggers_size))
