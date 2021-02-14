"""
In this assignment you will implement one or more algorithms for the traveling salesman
problem, such as the dynamic programming algorithm covered in the video lectures.  Here
is a data file describing a TSP instance: c04_w02_homework_input.txt

The first line indicates the number of cities.  Each city is a point in the plane, and
each subsequent line indicates the x- and y-coordinates of a single city.

The distance between two cities is defined as the Euclidean distance --- that is, two
cities at locations (x,y) and (z,w) have distance sqrt{(x-z)^2 + (y-w)^2} between them.

In the box below, type in the minimum cost of a traveling salesman tour for this
instance, rounded down to the nearest integer.

OPTIONAL: If you want bigger data sets to play with, check out the TSP instances from
around the world here.  The smallest data set (Western Sahara) has 29 cities, and most
of the data sets are much bigger than that.  What's the largest of these data sets that
you're able to solve --- using dynamic programming or, if you like, a completely
different method?

HINT: You might experiment with ways to reduce the data set size.  For example, trying
plotting the points.  Can you infer any structure of the optimal solution?  Can you use
that structure to speed up your algorithm?

CORRECT ANSWER: 26442
"""
from dataclasses import dataclass
from itertools import combinations
import math
import sys

from tqdm import tqdm


def get_cities_coordinates(filename):
    with open(filename) as cities_file:
        total_cities, *cities_coordinates = cities_file.readlines()

    cities = []
    for city in cities_coordinates:
        x, y = map(float, city.split())
        cities.append((x, y))

    assert len(cities) == int(total_cities)

    return cities


@dataclass
class TravelingSalesmanProblem:
    cities_coordinates: list
    euclidean_distances: dict

    def calc_euclidean_distance(self, city1: int, city2: int):
        if (city1, city2) not in self.euclidean_distances:
            x1, y1 = self.cities_coordinates[city1]
            x2, y2 = self.cities_coordinates[city2]

            distance = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
            self.euclidean_distances[(city1, city2)] = distance
            self.euclidean_distances[(city2, city1)] = distance

        return self.euclidean_distances[(city1, city2)]



    def solve(self):
        total_cities = len(self.cities_coordinates)  # this is n

        # partial_solutions is a "2D array" indexed by:
        #    - a subset (tuple) of visited cities S included in {0, 2, ..., n-1}
        #    - destination j wich belongs to {0, 2, ...., n-1}

        # BASE CASE = all cities, excluding initial (0) with the of going from
        # 0 to that city
        partial_solutions = {
            (city,): {city: self.calc_euclidean_distance(0, city)}
            for city in range(1, total_cities)
        }

        for problem_size in tqdm(range(2, total_cities)):
            for visited_cities in combinations(range(1, total_cities), problem_size):
                partial_solutions[visited_cities] = {}
                for last_visited in visited_cities:
                    subset_without_destination = tuple(
                        city for city in visited_cities if city != last_visited
                    )
                    partial_solutions[visited_cities][last_visited] = min(
                        (
                            partial_solutions[subset_without_destination][last_dest]
                            + self.calc_euclidean_distance(last_dest, last_visited)
                        )
                        for last_dest in subset_without_destination
                    )

        print(partial_solutions)
        return min(
            (
                partial_solutions[tuple(range(1, total_cities))][last_city]
                + self.calc_euclidean_distance(last_city, 0)
            )
            for last_city in range(1, total_cities)
        )

if __name__ == "__main__":
    filename = sys.argv[1]
    cities = get_cities_coordinates(filename)
    problem = TravelingSalesmanProblem(cities, {})
    print(problem.solve())
