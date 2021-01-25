"""
1. In this programming problem and the next you'll code up the greedy algorithm from the
lectures on Huffman coding.

Use the file c03_w03_homework_input_1.txt

This file describes an instance of the problem. It has the following format:

[number_of_symbols]
[weight of symbol #1]
[weight of symbol #2]
...

For example, the third line of the file is "6852892," indicating that the weight of the
second symbol of the alphabet is 6852892.  (We're using weights instead of frequencies,
like in the "A More Complex Example" video.)

Your task in this problem is to run the Huffman coding algorithm from lecture on this
data set. What is the maximum length of a codeword in the resulting Huffman code?

ADVICE: If you're not getting the correct answer, try debugging your algorithm using
some small test cases. And then post them to the discussion forum!

2. Continuing the previous problem, what is the minimum length of a codeword in your
Huffman code?
"""
import sys
from dataclasses import dataclass, field
from heapq import heappop, heappush


@dataclass(order=True)
class Tree:
    symbols: tuple = field(compare=False)
    weight: int


@dataclass
class HuffmanCoding:
    filename: str

    def __post_init__(self):
        with open(self.filename) as file:
            total_symbols, *weights = file.readlines()

        self.trees = []
        self.codes = {}
        for index, weight in enumerate(weights):
            heappush(self.trees, Tree((index,), int(weight)))
            self.codes[index] = ""

        self.total_symbols = int(total_symbols)

        assert len(self.trees) == self.total_symbols

    def create_tree(self):
        while len(self.trees) > 1:
            tree_1 = heappop(self.trees)
            tree_2 = heappop(self.trees)

            for symbol in tree_1.symbols:
                self.codes[symbol] = "0" + self.codes[symbol]
            for symbol in tree_2.symbols:
                self.codes[symbol] = "1" + self.codes[symbol]

            new_tree = Tree(
                symbols=tree_1.symbols + tree_2.symbols,
                weight=tree_1.weight + tree_2.weight,
            )
            heappush(self.trees, new_tree)


if __name__ == "__main__":
    filename = sys.argv[1]
    huffman = HuffmanCoding(filename)
    huffman.create_tree()

    symbols_size = [len(code) for code in huffman.codes.values()]

    print(f"max size symbol: {max(symbols_size)}")
    print(f"min size symbol: {min(symbols_size)}")

