import sys

def merge_and_count(first_half, second_half):
    inversions = 0

    sorted_list = []

    while first_half and second_half:
        if first_half[0] < second_half[0]:
            sorted_list.append(first_half.pop(0))
        else:
            sorted_list.append(second_half.pop(0))
            inversions += len(first_half)

    sorted_list.extend(first_half)
    sorted_list.extend(second_half)

    return inversions, sorted_list


def sort_and_count(a_list):
    size = len(a_list)
    if size == 1:
        return 0, a_list

    half_size = size // 2

    inversions_1, sorted_first_half = sort_and_count(a_list[:half_size])
    inversions_2, sorted_second_half = sort_and_count(a_list[half_size:])

    inversions_split, sorted_list = merge_and_count(sorted_first_half, sorted_second_half)

    total_inversions =  inversions_1 + inversions_2 + inversions_split

    return total_inversions, sorted_list


def get_list_from_file(filepath):
    with open(filepath) as file:
        raw_numbers = file.readlines()

    return [int(number.strip()) for number in raw_numbers]


if __name__ == "__main__":
    try:
        input_list = [int(x) for x in sys.argv[1:]]

        print(sort_and_count(input_list))
    except ValueError:
        file_path = sys.argv[1]
        print(f"Procesing the file {file_path}")

        input_list = get_list_from_file(file_path)
        print(f"Received a list of {len(input_list)} elements")

        inversions, _ = sort_and_count(input_list)
        print(f"Total inversions: {inversions}")
