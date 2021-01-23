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
import pickle
import sys
from dataclasses import dataclass

from tqdm import tqdm

from c03_w02_clustering_algorithm_1 import UnionFindClusters, SameClusterUnionError


@dataclass
class BigClusteringProblem:
    filename: str

    backup_init_file = "c03_w02_backup_init.json"

    def __post_init__(self):
        processed_lines, all_nodes, near_nodes = self._restore_init()
        self.distance_lower_than_three = near_nodes

        with open(self.filename) as datafile:
            info, *nodes = datafile.readlines()
            nodes_quantity, bits = info.split()
            self.bits_for_node = int(bits)
            self.nodes_quantity = int(nodes_quantity)

            for index, line in tqdm(enumerate(nodes)):
                if index < processed_lines:
                    continue
                current_node = tuple(line.split())
                for other_node in all_nodes:
                    hamming_distance = 0
                    for x in range(self.bits_for_node):
                        if current_node[x] != other_node[x]:
                            hamming_distance +=1
                            if hamming_distance > 2:
                                break
                    else:
                        self.distance_lower_than_three.append((current_node, other_node))

                all_nodes.add(current_node)

                if index % 1000 == 0:
                    self._backup(index, all_nodes, self.distance_lower_than_three)

        self.clusters = UnionFindClusters(all_nodes)

    def _restore_init(self):
        try:
            with open(self.backup_init_file, "rb") as backup_file:
                data = pickle.load(backup_file)
        except FileNotFoundError:
            data = {}

        if data:
            return data["processed_lines"], data["all_nodes"], data["near_nodes"]

        return -1, set(), list()


    def _backup(self, processed_lines, all_nodes, near_nodes):
        backup = {
            "processed_lines": processed_lines,
            "all_nodes": all_nodes,
            "near_nodes": near_nodes,
        }
        with open(self.backup_init_file, "wb") as backup_file:
            pickle.dump(backup, backup_file)


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
