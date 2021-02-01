"""
Consider an instance of the optimal binary search tree problem with 7 keys (say
1,2,3,4,5,6,7 in sorted order) and frequencies w_1 = .05, w_2 = .4, w_3 = .08,
w_4 = .04, w_5 = .1, w_6 = .1, w_7 = .23

What is the minimum-possible average search time of a binary search tree with these
keys?
"""
import numpy

def binary_search_tree(weights=None):
    if weights is None:
        weights = [0.05, 0.4, 0.08, 0.04, 0.1, 0.1, 0.23]
    n = len(weights)

    partial_bst = numpy.zeros((n, n))# partial_bst[i][j] is opt BST of items {i, ..., j}

    for s in range(n):
        for i in range(n):
            j = i + s
            if j >= n:
                print(f"continue i={i} y j={j}")
                continue
            to_get_min = []
            for r in range(i, j+1):
                left_tree = 0
                right_tree = 0
                if i <= r-1:
                    left_tree = partial_bst[i][r-1]
                if r + 1 <= j and r+1 < n:
                    right_tree = partial_bst[r+1][j]
                to_get_min.append(left_tree + right_tree)

            partial_bst[i][j] = sum(weights[i:j+1]) + min(to_get_min)
            print(f"{i} - {j}")
            print(partial_bst)
            input()

    return partial_bst[0][n-1]



if __name__ == "__main__":
    web_example = [4, 2, 6, 3]  # expected result=26
    final_exam = [0.2, 0.05, 0.17, 0.1, 0.2, 0.03, 0.25]  # Expected result = 2.23
    result = binary_search_tree(final_exam)
    # Expected result with default weights=2.18
    print(f"Result = {result}")



