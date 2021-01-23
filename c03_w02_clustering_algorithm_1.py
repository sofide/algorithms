"""
In this programming problem and the next you'll code up the clustering algorithm from
lecture for computing a max-spacing kk-clustering.

Use the file c03_w02_homework_input_1.txt

This file describes a distance function (equivalently, a complete graph with edge
costs).  It has the following format:

[number_of_nodes]

[edge 1 node 1] [edge 1 node 2] [edge 1 cost]

[edge 2 node 1] [edge 2 node 2] [edge 2 cost]

...

There is one edge (i,j) for each choice of 1 < i < j <= n, where nn is the number of
nodes.

For example, the third line of the file is "1 3 5250", indicating that the distance
between nodes 1 and 3 (equivalently, the cost of the edge (1,3)) is 5250.  You can
assume that distances are positive, but you should NOT assume that they are distinct.

Your task in this problem is to run the clustering algorithm from lecture on this data
set, where the target number kk of clusters is set to 4.  What is the maximum spacing of
a 4-clustering?

ADVICE: If you're not getting the correct answer, try debugging your algorithm using
some small test cases.  And then post them to the discussion forum!
"""
import sys
from dataclasses import dataclass, field
from heapq import heappush, heappop

class SameClusterUnionError(Exception):
    pass


@dataclass
class UnionFindClusters:
    cluster_heads: set = field(default_factory=set)
    nodes_parents: dict = field(default_factory=dict)
    nodes_size: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.nodes_parents:
            for node in self.cluster_heads:
                self.nodes_parents[node] = node
                self.nodes_size[node] = 0

    def find(self, node):
        parent = self.nodes_parents[node]

        while parent != node:
            node = parent
            parent = self.nodes_parents[node]

        return parent

    def union(self, node_one, node_two):
        parent_one = self.find(node_one)
        parent_two = self.find(node_two)

        if parent_one == parent_two:
            raise SameClusterUnionError

        parent_one_size = self.nodes_size[parent_one]
        parent_two_size = self.nodes_size[parent_two]

        if parent_one_size > parent_two_size:
            common_parent = parent_one
            self.nodes_parents[parent_two] = parent_one
            self.cluster_heads.remove(parent_two)
        elif parent_two_size > parent_one_size:
            common_parent = parent_two
            self.nodes_parents[parent_one] = parent_two
            self.cluster_heads.remove(parent_one)
        else:
            # parent_one and parent_two have the same size
            common_parent = parent_one
            self.nodes_parents[parent_two] = parent_one
            self.cluster_heads.remove(parent_two)
            # common_parent node will have a new level
            self.nodes_size[parent_one] += 1

        return common_parent

    def same_cluster(self, node_1, node_2):
        parent_1 = self.find(node_1)
        parent_2 = self.find(node_2)

        return parent_1 == parent_2


@dataclass(order=True)
class Edge:
    nodes: set = field(compare=False)
    size: int


@dataclass
class ClusteringProblem:
    filename: str
    heapq_edges: list = field(default_factory=list)

    def __post_init__(self):
        all_nodes = set()
        with open(self.filename) as datafile:
            _, *edges = datafile.readlines()

        for edge in edges:
            node_1, node_2, edge_size = edge.split()
            new_edge = Edge({node_1, node_2}, int(edge_size))
            all_nodes.update(new_edge.nodes)
            heappush(self.heapq_edges, new_edge)

        self.clusters = UnionFindClusters(all_nodes)

    @property
    def spacing(self):
        while True:
            edge = heappop(self.heapq_edges)
            if not self.clusters.same_cluster(*edge.nodes):
                heappush(self.heapq_edges, edge)

                return edge.size

    def merge_closest_clusters(self):
        while True:
            min_edge = heappop(self.heapq_edges)
            try:
                common_parent = self.clusters.union(*min_edge.nodes)
                break
            except SameClusterUnionError:
                pass

        return common_parent


    def k_clusters(self, k: int):
        while len(self.clusters.cluster_heads) > k:
            self.merge_closest_clusters()


if __name__ == "__main__":
    filename = sys.argv[1]

    print("Initializing problem")
    problem = ClusteringProblem(filename)

    print("Merging clusters")
    problem.k_clusters(4)

    print(f"Max spacing for 4 clusters: {problem.spacing}")
