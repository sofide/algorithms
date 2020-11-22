import math
import sys

import pytest


def multiply_karatsuba(x, y):
    x_str = str(x)
    y_str = str(y)

    size_x = len(x_str)
    size_y = len(y_str)

    size = max(size_x, size_y)

    if size == 1:
        return x * y

    if size % 2 != 0:
        size += 1

    x_str = "0" * (size - size_x) + x_str
    y_str = "0" * (size - size_y) + y_str

    half_size = int(size/2)

    x_a = int(x_str[:half_size])
    x_b = int(x_str[half_size:])
    y_a = int(y_str[:half_size])
    y_b = int(y_str[half_size:])

    step_1 = multiply_karatsuba(x_a, y_a)
    step_2 = multiply_karatsuba(x_b, y_b)
    step_3 = multiply_karatsuba(x_a + x_b, y_a + y_b)
    step_4 = step_3 - step_2 - step_1

    addend_1 = step_1 * (10 ** size)
    addend_2 = step_4 * (10 ** half_size)
    addend_3 = step_2

    result = addend_1 + addend_2 + addend_3

    return result



@pytest.mark.parametrize("x,y,result", [
    (20, 1, 20),
    (88, 27, 2376),
    (3, 4, 12),
    (10, 10, 100),
    (10, 20, 200),
    (1000, 1000, 1000000),
    (8888, 2727, 24237576),
    (272727, 442, 120545334),
    (2718281828459045235360287471352662497757247093699959574966967627,
     3141592653589793238462643383279502884197169399375105820974944592,
     8539734222673567065463550869546574495034888535765114961879601127067743044893204848617875072216249073013374895871952806582723184,
     )
])
def test_multiply_karatsuba(x, y, result):
    assert multiply_karatsuba(x, y) == result


if __name__ == "__main__":
    _, _x, _y = sys.argv

    print(multiply_karatsuba(int(_x), int(_y)))
