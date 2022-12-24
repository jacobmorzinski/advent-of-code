#!/usr/bin/env python

# https://adventofcode.com/2015/day/2

# part1
# How many total square feet of wrapping paper should they order?

# part2
# How many total feet of ribbon should they order?


import argparse
import sys
import unittest

## python -m unittest day2
class TestInputs(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1x1x10(self):
        area, length = find_needed_area("1x1x10")
        self.assertEqual(area, 43)
        self.assertEqual(length, 14)

    def test_2x3x4(self):
        area, length = find_needed_area("2x3x4")
        self.assertEqual(area, 58)
        self.assertEqual(length, 34)


def find_needed_area(dimensions):
    """2*l*w + 2*w*h + 2*h*l
    plus the area of the smallest side"""
    
    l,w,h = dimensions.split("x")
    l,w,h = map(int, (l,w,h))
    area = 2*l*w + 2*w*h + 2*h*l

    dims = sorted((l,w,h))
    extra = dims[0] * dims[1]

    ribbon_length = find_ribbon_length(dims)

    return area + extra, ribbon_length


def find_ribbon_length(dims):
    ribbon_for_bow = dims[0] * dims[1] * dims[2]
    ribbon_for_sides = 2 * dims[0] + 2 * dims[1]
    return ribbon_for_sides + ribbon_for_bow


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    total_area = 0
    total_length = 0
    with open(args.input, "r") as f:
        for line in f:
            line = line.strip()
            area, length = find_needed_area(line)
            total_area += area
            total_length += length

    print(f"area is {total_area}")
    print(f"length is {total_length}")


if __name__ == "__main__":
    sys.exit(main())

