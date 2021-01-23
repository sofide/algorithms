"""
In this question your task is again to run the clustering algorithm from lecture, but on
a MUCH bigger graph.  So big, in fact, that the distances (i.e., edge costs) are only
defined implicitly, rather than being provided as an explicit list.

Use the file c03_w02_homework_input_2.txt

The format is:

[# of nodes] [# of bits for each node's label]

[first bit of node 1] ... [last bit of node 1]

[first bit of node 2] ... [last bit of node 2]

...

For example, the third line of the file
"0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1" denotes the 24 bits associated with
node #2.

The distance between two nodes u and v in this problem is defined as the Hamming
distance--- the number of differing bits --- between the two nodes' labels.  For
example, the Hamming distance between the 24-bit label of node #2 above and the label
"0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3 (since they differ in the 3rd,
7th, and 21st bits).

The question is: what is the largest value of kk such that there is a kk-clustering
with spacing at least 3?  That is, how many clusters are needed to ensure that no pair
of nodes with all but 2 bits in common get split into different clusters?

NOTE: The graph implicitly defined by the data file is so big that you probably can't
write it out explicitly, let alone sort the edges by cost.  So you will have to be a
little creative to complete this part of the question.  For example, is there some way
you can identify the smallest distances without explicitly looking at every pair of
nodes?
"""
import sys
from dataclasses import dataclass

import tqdm

from c03_w02_clustering_algorithm_1 import UnionFindClusters, SameClusterUnionError


@dataclass
class BigClusteringProblem:
    filename: str

    def __post_init__(self):
        all_nodes = set()
        self.distance_of_one = []
        self.distance_of_two = []

        with open(self.filename) as datafile:
            for index, line in enumerate(datafile.readlines()):
                if index == 0:
                    nodes_quantity, bits = line.split()
                    self.bits_for_node = int(bits)
                    self.nodes_quantity = int(nodes_quantity)
                    continue

                current_node = tuple(line.split())
                for other_node in all_nodes:
                    distance = self.hamming_distance(current_node, other_node)
                    if distance == 1:
                        self.distance_of_one.append((current_node, other_node))
                    elif distance == 2:
                        self.distance_of_two.append((current_node, other_node))

                all_nodes.add(current_node)

        self.clusters = UnionFindClusters(all_nodes)

    def hamming_distance(self, node_1: tuple, node_2: tuple):
        diff_bits = [x for x in range(self.bits_for_node) if node_1[x] != node_2[x]]
        return len(diff_bits)

    def _force_union(self, nodes):
        try:
            self.clusters.union(*nodes)
        except SameClusterUnionError:
            pass

    def merge_until_spacing_of_three(self):
        for nodes in self.distance_of_one:
            self._force_union(nodes)

        for nodes in self.distance_of_two:
            self._force_union(nodes)


if __name__ == "__main__":
    filename = sys.argv[1]

    print("Initializing problem")
    problem = BigClusteringProblem(filename)

    print("Merging clusters")
    problem.merge_until_spacing_of_three()

    print(f"Number of clusters after merging: {len(problem.clusters.cluster_heads)}")
