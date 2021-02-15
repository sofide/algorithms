"""
In this assignment we will revisit an old friend, the traveling salesman problem (TSP).
This week you will implement a heuristic for the TSP, rather than an exact algorithm,
and as a result will be able to handle much larger problem sizes.  Here is a data file
describing a TSP instance (original source:
http://www.math.uwaterloo.ca/tsp/world/bm33708.tsp).

c04_w03_homework_input.txt

The first line indicates the number of cities. Each city is a point in the plane, and
each subsequent line indicates the x- and y-coordinates of a single city.

The distance between two cities is defined as the Euclidean distance --- that is, two
cities at locations (x,y)(x,y) and (z,w)(z,w) have distance sqrt{(x-z)^2 + (y-w)^2}
between them.

You should implement the nearest neighbor heuristic:

1. Start the tour at the first city.

2. Repeatedly visit the closest city that the tour hasn't visited yet.  In case of a
tie, go to the closest city with the lowest index.  For example, if both the third and
fifth cities have the same distance from the first city (and are closer than any other
city), then the tour should begin by going from the first city to the third city.

3. Once every city has been visited exactly once, return to the first city to complete
the tour.

In the box below, enter the cost of the traveling salesman tour computed by the nearest
neighbor heuristic for this instance, rounded down to the nearest integer.

[Hint: when constructing the tour, you might find it simpler to work with squared
Euclidean distances (i.e., the formula above but without the square root) than
Euclidean distances.  But don't forget to report the length of the tour in terms of
standard Euclidean distance.]

CORRECT ANSWER = 1203406
"""
from dataclasses import dataclass, field
import math
import sys

import numpy
from tqdm import tqdm


def get_cities_coordinates(filename):
    with open(filename) as cities_file:
        total_cities, *cities_coordinates = cities_file.readlines()

    cities = []
    for city in cities_coordinates:
        _, x, y = map(float, city.split())
        cities.append((x, y))

    assert len(cities) == int(total_cities)

    return cities


@dataclass
class TravelingSalesmanHeuristic:
    cities_coordinates: list

    def calc_euclidean_distance(self, city1: int, city2: int):
        x1, y1 = city1
        x2, y2 = city2

        return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

    def heuristic(self):
        first_city = self.cities_coordinates.pop(0)
        last_visited_city = first_city

        path_length = 0

        pbar = tqdm(total=len(self.cities_coordinates))

        while self.cities_coordinates:
            nearest_distance = numpy.inf
            nearest_index = None

            for index, city in enumerate(self.cities_coordinates):
                distance = self.calc_euclidean_distance(last_visited_city, city)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_index = index

            path_length += nearest_distance
            last_visited_city = self.cities_coordinates.pop(nearest_index)
            pbar.update(1)

        # return home
        path_length += self.calc_euclidean_distance(last_visited_city, first_city)

        return path_length


if __name__ == "__main__":
    filename = sys.argv[1]

    cities = get_cities_coordinates(filename)

    problem = TravelingSalesmanHeuristic(cities)

    print(problem.heuristic())
