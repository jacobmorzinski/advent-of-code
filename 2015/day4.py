#!/usr/bin/env python

# https://adventofcode.com/2015/day/4

# part1
# find Santa the lowest positive number that produces such a hash

# part2
# find a hash with six leading zeroes


import argparse
import sys
import unittest
import hashlib


## python -m unittest day4
class TestInputs(unittest.TestCase):
    """
    If your secret key is abcdef, the answer is 609043, because the MD5 hash of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest such number to do so.
    If your secret key is pqrstuv, the lowest number it combines with to make an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_part1(self):
        low_number = find_low_number("abcdef", 5)
        self.assertEqual(low_number, 609043)
        low_number = find_low_number("pqrstuv", 5)
        self.assertEqual(low_number, 1048970)

    def test_part2(self):
        pass


def find_low_number(prefix, digits):
    target = str(0) * digits
    b_prefix = prefix.encode("utf-8")
    for i in range(0, 2_000_000):
        b_suffix = str(i).encode("utf-8")
        b_input = b''.join([b_prefix, b_suffix])
        hash = hashlib.md5(b_input).hexdigest()
        if hash.startswith(target):
            return i

        
def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    with open(args.input, "r") as f:
        for line in f:
            line = line.strip()
            puzzle_input = line
            low_number = find_low_number(puzzle_input, 5)
            print(f"low_number for five zeroes is {low_number}")
            low_number = find_low_number(puzzle_input, 6)
            print(f"low_number for six zeroes is {low_number}")


if __name__ == "__main__":
    sys.exit(main())

