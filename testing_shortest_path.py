import sys
from time import time

from c04_w01_all_pairs_shortest_paths_johnson import DijkstraShortestPath, BellmanFord


def get_graph_from_file(filename):
    graph = {}
    with open(filename) as file:
        for line in file.readlines():
            tail, *edges = line.split()
            edges = [edge.split(",") for edge in edges]
            graph[tail] = {head: int(length) for head, length in edges}

    return graph


if __name__ == "__main__":
    starting_time = time()
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        filename = "c02_w02_input_file.txt"

    graph = get_graph_from_file(filename)

    starting_time = time()
    dijkstra = DijkstraShortestPath(graph, "1")
    dijkstra_sol = dijkstra.calc_shortest_path()

    bellman = BellmanFord(graph, "1")
    bellman_sol = bellman.solve()


    # print(f"shortest path: {problem.shortest_path}")

    nodes_to_report = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    print("solution dijkstra:")
    dijkstra_report = [dijkstra_sol[str(vertex)] for vertex in nodes_to_report]
    print(dijkstra_report)
    print("solution bellman:")
    bellman_report = [bellman_sol[str(vertex)] for vertex in nodes_to_report]
    print(bellman_report)
    end_time = time()

    expected = [2599, 2610, 2947, 2052, 2367, 2399, 2029, 2442, 2505, 3068]
    assert dijkstra_report == expected
    assert bellman_report == expected
    print("✅ everything as expected")

    print(f"Running time: {end_time - starting_time}")
