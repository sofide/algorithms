"""
Binary tree will be represented as a dict with the following structure:
{
    "root": node,
    node_x: {
        parent: node or None,
        left_child: node or None,
        right_child: node or None,
        size: # of nodes in subtree rooted in node_x
    }
}

So, for example, this tree:
            [3]
           /   \
          /     [5]
        [1]     /
           \   [4]
           [2]

will be represented as:

{
    "root": 3,
    3: {
        "parent": None,
        "left_child": 1,
        "right_child": 5,
        "size": 5,
    },
    1: {
        "parent": 3,
        "left_child": None,
        "right_child": 2,
        "size": 2,
    },
    ...
}
"""
import math
import sys
import time


PARENT_KEY = "parent"
LEFT_CHILD_KEY = "left_child"
RIGHT_CHILD_KEY = "right_child"
SIZE_KEY = "size"

ROOT_KEY = "root"


def insert_in_tree(tree, element):
    if ROOT_KEY not in tree:
        tree[ROOT_KEY] = element
        tree[element] = {
            PARENT_KEY: None,
            LEFT_CHILD_KEY: None,
            RIGHT_CHILD_KEY: None,
            SIZE_KEY: 1,
        }
        return

    parent = tree[ROOT_KEY]

    while True:
        tree[parent][SIZE_KEY] += 1
        if element <= parent:
            new_parent = tree[parent][LEFT_CHILD_KEY]
            child_direction = LEFT_CHILD_KEY
        else:
            new_parent = tree[parent][RIGHT_CHILD_KEY]
            child_direction = RIGHT_CHILD_KEY

        if new_parent is None:
            break

        parent = new_parent

    tree[parent][child_direction] = element
    tree[element] = {
        PARENT_KEY: parent,
        LEFT_CHILD_KEY: None,
        RIGHT_CHILD_KEY: None,
        SIZE_KEY: 1,
    }


def find_median(tree):
    median_position = math.ceil((len(tree) -1) / 2)
    current_root = tree[ROOT_KEY]
    current_position = 0

    while True:
        left_child = tree[current_root][LEFT_CHILD_KEY]
        if left_child:
            root_subtree_position = tree[left_child][SIZE_KEY] + 1
        else:
            root_subtree_position = 1

        current_position += root_subtree_position
        if median_position == current_position:
            return current_root

        if median_position < current_position:
            current_root = left_child
            current_position -= root_subtree_position

        else:
            current_root = tree[current_root][RIGHT_CHILD_KEY]


def median_with_binary_tree(input_list):
    tree = {}
    medians = []

    for number in input_list:
        insert_in_tree(tree, number)
        medians.append(find_median(tree))

    return medians


def get_input_from_file(filename: str):
    with open(filename) as file:
        input_list = [int(number) for number in file.readlines()]

    return input_list


def solve_homework(input_list):
    medians = median_with_binary_tree(input_list)

    medians_sum = sum(medians)

    return medians_sum % 10000


if __name__ == "__main__":
    start_time = time.time()
    input_file = sys.argv[1]

    print(f"Reading file {input_file}...")
    input_list = get_input_from_file(input_file)

    print("solving homework...")
    result = solve_homework(input_list)

    print(f"Result: {result}")

    end_time = time.time()
    print(f"calculated in {end_time - start_time} seconds")
