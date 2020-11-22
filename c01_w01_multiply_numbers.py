"""
Assignment for first week of "Divide and Conquer" course.
---------------------------------------------------------

In this programming assignment you will implement one or more of the integer
multiplication algorithms described in lecture.

To get the most out of this assignment, your program should restrict itself to
multiplying only pairs of single-digit numbers. You can implement the grade-school
algorithm if you want, but to get the most out of the assignment you'll want to
implement recursive integer multiplication and/or Karatsuba's algorithm.

So: what's the product of the following two 64-digit numbers?

3141592653589793238462643383279502884197169399375105820974944592

2718281828459045235360287471352662497757247093699959574966967627
"""
import math
import sys


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


if __name__ == "__main__":
    _, _x, _y = sys.argv

    print(multiply_karatsuba(int(_x), int(_y)))
