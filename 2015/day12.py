#!/usr/bin/env python

# https://adventofcode.com/2015/day/12

# part1
# What is the sum of all numbers in the document?

# part2
# Ignore any object (and all of its children) which has any property with the value "red".


import argparse
import sys
import unittest
import re
import json
import functools


## python -m unittest day12
class TestInputs(unittest.TestCase):
    """

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_part1(self):
        self.assertEqual(number_sum([1,2,3]), 6)
        self.assertEqual(number_sum({"a":2,"b":4}), 6)
        self.assertEqual(number_sum([[[3]]]), 3)
        self.assertEqual(number_sum({"a":{"b":4},"c":-1}), 3)
        self.assertEqual(number_sum({"a":[-1,1]}), 0)
        self.assertEqual(number_sum([-1,{"a":1}]), 0)
        self.assertEqual(number_sum([]), 0)
        self.assertEqual(number_sum({}), 0)

    def test_part2(self):
        self.assertEqual(number_sum([1,2,3], "red"), 6)
        self.assertEqual(number_sum([1,{"c":"red","b":2},3], "red"), 4)
        self.assertEqual(number_sum({"d":"red","e":[1,2,3,4],"f":5}, "red"), 0)
        self.assertEqual(number_sum([1,"red",5], "red"), 6)


def number_sum(item, ignore_color=None):
    """Recursively process an item, summing all numbers found.
    If ignore_color is given, ignore objects which have a property
    whose value is the ignore_color."""
    total = 0

    # a convenience function so we can call map(...) using it.
    number_sum_partial = functools.partial(number_sum, ignore_color=ignore_color)

    if isinstance(item, int):
        total += item
    elif isinstance(item, list):
        total += sum(map(number_sum_partial, item))
    elif isinstance(item, dict):
        if ignore_color in item.values():
            pass
        else:
            total += sum(map(number_sum_partial, item.values()))
    elif isinstance(item, str):
        pass
    else:
        print(item)
        raise(Exception(f"Unhandled type {type(item)}"))

    return total


def part1(input_stream):
    total = 0
    for line in input_stream:
        j = line.strip()
        d = json.loads(j)
        total = number_sum(d)
    return total


def part2(input_stream):
    total = 0
    for line in input_stream:
        j = line.strip()
        d = json.loads(j)
        total = number_sum(d, ignore_color="red")
    return total


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        result = part1(f)
    print(f"part 1: the sum of all numbers is {result}")

    with open(args.input, "r") as f:
        result = part2(f)
    print(f"part 2: the sum of all numbers ignoring red is {result}")


if __name__ == "__main__":
    sys.exit(main())

