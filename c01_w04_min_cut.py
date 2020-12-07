"""
The file contains the adjacency list representation of a simple undirected graph. There
are 200 vertices labeled 1 to 200. The first column in the file represents the vertex
label, and the particular row (other entries except the first column) tells all the
vertices that the vertex is adjacent to. So for example, the 6th row looks like:
"6 155 56 52 120 ......". This just means that the vertex with label 6 is adjacent to
(i.e., shares an edge with) the vertices with labels 155,56,52,120,......, etc.

Your task is to code up and run the randomized contraction algorithm for the min cut
problem and use it on the above graph to compute the min cut. (HINT: Note that you'll
have to figure out an implementation of edge contractions. Initially, you might want to
do this naively, creating a new graph from the old every time there's an edge
contraction. But you should also think about more efficient implementations.)
(WARNING: As per the video lectures, please make sure to run the algorithm many times
with different random seeds, and remember the smallest cut that you ever find.) Write
your numeric answer in the space provided. So e.g., if your answer is 5, just type 5 in
the space provided.
"""
import logging
import random
import sys

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def graph_from_file(filename):
    with open(filename) as file:
        matrix = [row.split() for row in file.readlines()]

    graph_dict = {}

    for row in matrix:
        graph_dict[row[0]] = row[1:]

    return graph_dict


def pick_a_random_edge(graph):
    v1 = random.choice(list(graph))
    v2 = random.choice(graph[v1])

    return v1, v2


def rename_vertex(graph, old_vertex, new_vertex, adjacent_vertices):
    for adj_vertex in adjacent_vertices:
        adj_vertex_edges = graph[adj_vertex]
        q_vertex_edges = len(adj_vertex_edges)

        graph[adj_vertex] = [edge for edge in adj_vertex_edges if edge != old_vertex]
        q_other_edges = len(graph[adj_vertex])
        q_renamed_vertex_edges = q_vertex_edges - q_other_edges

        graph[adj_vertex] += ([new_vertex] * q_renamed_vertex_edges)

    return graph


def random_contraction(graph, depth=0):
    inden = " " * depth * 4
    logger.debug("%s----- INIT DEPTH %s -----", inden, depth)
    logger.debug("%sGRAPH: %s", inden, graph)
    if len(graph) == 2:
        values = list(graph.values())
        assert len(values[0]) == len(values[1])
        logger.debug("%sRETURN crossing edges: %s", inden, len(values[0]))
        return len(values[0])

    v1, v2 = pick_a_random_edge(graph)

    logger.debug("%sv1: %s - v2: %s", inden, v1, v2)

    v1_edges = graph.pop(v1)
    v2_edges = graph.pop(v2)

    # remove self loops
    v1_edges = [edge for edge in v1_edges if edge != v2]
    v2_edges = [edge for edge in v2_edges if edge != v1]

    new_vertex = f"{v1} {v2}"

    new_vertex_adj = v1_edges + v2_edges
    graph[new_vertex] = new_vertex_adj

    # rename v1 and v2 adj references to new vertex
    graph = rename_vertex(graph, v1, new_vertex, v1_edges)
    graph = rename_vertex(graph, v2, new_vertex, v2_edges)

    logger.debug("%sRENAMED GRAPH: %s", inden, graph)

    return random_contraction(graph, depth+1)


if __name__ == "__main__":
    if "-v" in sys.argv:
        logger.info("debug mode activated")
        sys.argv.remove("-v")
        logger.setLevel(logging.DEBUG)

    filename = sys.argv[1]

    graph = graph_from_file(filename)

    crossing_edges = random_contraction(graph)

    print(f"{crossing_edges=}")
