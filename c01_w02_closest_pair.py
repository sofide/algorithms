from itertools import combinations


def distance(point_a, point_b):
    a_x, a_y = point_a
    b_x, b_y = point_b

    # euclidean distance
    return (((a_x - b_x) ** 2) + (a_y - b_y) ** 2) ** 0.5


def get_splited_closest(points_by_x, points_by_y, delta):
    half_size = len(points_by_x) // 2

    med_x = points_by_x[half_size-1][0]  # the most right point on the left half orderer by x

    x_lower_bound  = med_x - delta
    x_upper_bound  = med_x + delta

    posible_points = [
        (x, y) for x, y in points_by_y
        if x >= x_lower_bound
        and x <= x_upper_bound
    ]

    best_distance = delta
    best_pair = None

    for i, point_a in enumerate(posible_points):
        # if there is a pair with a distance lower than delta, it must be at max at 7
        # positions of distance according to the Lemma learned in this lection.
        for point_b in posible_points[i+1: i+8]:
            a_b_distance = distance(point_a, point_b)
            if a_b_distance < best_distance:
                best_distance = a_b_distance
                best_pair = point_a, point_b

    return best_pair


def force_brute_closest(points):
    points = [p for p in points if p is not None]

    best_distance = None
    for pair in combinations(points, 2):
        points_distance = distance(*pair)
        if best_distance is None or points_distance < best_distance:
            best_distance = points_distance
            best_pair = pair

    return best_pair


def get_closest_pair(points_by_x, points_by_y):
    """
    points_by_x and points_by_y are two list of the same points ordered by x and y
    respectibly
    """
    size = len(points_by_x)
    if size <= 3:
        return force_brute_closest(points_by_x)

    half_size = size // 2

    left_points_by_x = points_by_x[:half_size]
    right_points_by_x = points_by_x[half_size:]

    left_points_by_y = [point for point in points_by_y if point in left_points_by_x]
    right_points_by_y = [point for point in points_by_y if point in right_points_by_x]

    left_closest = get_closest_pair(left_points_by_x, left_points_by_y)
    right_closest = get_closest_pair(right_points_by_x, right_points_by_y)
    delta = min(distance(*left_closest), distance(*right_closest))

    splited_closest = get_splited_closest(points_by_x, points_by_y, delta)

    closest_points = [left_closest, right_closest]

    if splited_closest is not None:
        closest_points.append(splited_closest)

    closest_points.sort(key=lambda points: distance(*points))

    return closest_points[0]
