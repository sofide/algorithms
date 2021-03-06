"""
See "c04_w04_2_sat_algorithm.py" for the homework explanation.

Here I will try with the StronglyConnectedComponents approach.
"""
from collections import defaultdict, Counter
from dataclasses import dataclass
import sys

from tqdm import tqdm

from c04_w04_2_sat_algorithm import get_clauses_from_file

class InsolubleSATError(Exception):
    pass


def get_graph_from_filename(graph_filename):
    """
    Read graph from the given file
    """
    graph = defaultdict(list)

    with open(graph_filename) as f:
        for edge in f.readlines():
            tail, head = edge.split()
            graph[tail].append(head)

    return graph

def get_graph_from_clauses(clauses):
    """ Get a graph from 2-sat clauses.
    For example the clause (x1 or x2) means that if x1 is False, x2 must be True, and
    viceversa.

    So (x1, x2) clause will generate the following edges: (-x1, x2) and (-x2, x1)
    """
    graph = defaultdict(list)

    for var_1, var_2 in clauses:
        # create nodes in graph if they don't exists and do nothing if they were
        # already created)
        graph[var_1]
        graph[var_2]

        # add constraints to opposit nodes (if var_1 is false, var_2 must be true and
        # vice versa
        graph[var_1 * -1].append(var_2)
        graph[var_2 * -1].append(var_1)

    return dict(graph)

@dataclass
class StronglyConnectedComponents:
    graph: list[dict]

    @property
    def inverted_graph(self):
        """
        calc the inverted graph
        """
        if not hasattr(self, "_inverted_graph"):
            self._inverted_graph = defaultdict(list)

            for tail, heads in self.graph.items():
                for head in heads:
                    self._inverted_graph[head].append(tail)

        return self._inverted_graph


    @staticmethod
    def _scc_calc(graph, order=None, sat_scc=False):
        explored_vertices = set()
        finishing_order = []
        leaders_order = []

        def depth_first_search(graph, start):
            leaders_order.append(start)
            nodes_to_expand = [start]
            if sat_scc:
                components_in_scc = {start}

            starting_order = []

            while nodes_to_expand:
                tail = nodes_to_expand.pop(-1)
                if tail not in explored_vertices:
                    pbar.set_description(f"Nodes to expand {len(nodes_to_expand)}")
                    if not sat_scc:
                        # only populate this list in first iteration, to find the leaders
                        starting_order.append(tail)
                    explored_vertices.add(tail)

                    if sat_scc:
                        if tail * -1 in components_in_scc:
                            raise InsolubleSATError
                        components_in_scc.add(tail)

                    nodes_to_expand.extend(
                        [head for head in graph[tail] if head not in explored_vertices]
                    )

            starting_order.reverse()
            finishing_order.extend(starting_order)

        if not order:
            order = list(graph)

        pbar = tqdm(order)
        for node in pbar:
            if node not in explored_vertices:
                # print(f"leader {node}")
                depth_first_search(graph, node)

        return finishing_order

    def calc(self):
        """
        Compute all the strongly connected components (sccs) and return its leaders and
        size
        """
        finishing_order = self._scc_calc(self.inverted_graph)

        finishing_order.reverse()

        self._scc_calc(self.graph, finishing_order, sat_scc=True)


if __name__ == "__main__":
    filename = sys.argv[1]

    print(f"Calculate StronglyConnectedComponents from file {filename}")
    clauses = get_clauses_from_file(filename)
    graph = get_graph_from_clauses(clauses)
    sccs_problem = StronglyConnectedComponents(graph)

    try:
        sccs_problem.calc()
        print("✅ SOLUTION FOUND! This problem is soluble")
    except InsolubleSATError:
        print("❌ ERROR TRYING TO FIND A SOLUTION. This problem is not soluble")

