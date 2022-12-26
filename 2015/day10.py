#!/usr/bin/env python

# https://adventofcode.com/2015/day/10

# part1
# What is the length of the result?

# part2
# What is the length of the result?


import argparse
import sys
import unittest
import re


## python -m unittest day10
class TestInputs(unittest.TestCase):
    """

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_part1(self):
        inputs_outputs = {
            "1": "11",
            "11": "21",
            "21": "1211",
            "1211": "111221",
            "111221": "312211",
        }

        for look,say in inputs_outputs.items():
            with self.subTest(look=look, say=say):
                self.assertEqual(look_and_say(look), say)


    def test_part2(self):
        pass


def replace(m):
    n = m.group("n")
    count = len(m.group(0))
    return f"{count}{n}"


def look_and_say(look):
    s = look
    # (?P<n>\d) -> capture the \d in named group "n"
    # (?P=n) -> refer to named group "n" in the same pattern itself
    r = re.sub(r"(?P<n>\d)(?P=n)*", replace, s)
    # print(r)
    return r


def part1(input_stream):
    """
    """

    total = 0

    for line in input_stream:
        look = line.strip()
        for _ in range(40):
            say = look_and_say(look)
            # print(say)
            look = say

    return say


def part2(input_stream):
    """
    """

    total = 0

    for line in input_stream:
        look = line.strip()
        for _ in range(50):
            say = look_and_say(look)
            look = say

    return say


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    with open(args.input, "r") as f:
        result = part1(f)
    print(f"part 1: the length is {len(result)}")

    with open(args.input, "r") as f:
        result = part2(f)
    print(f"part 2: the length is {len(result)}")



if __name__ == "__main__":
    sys.exit(main())

