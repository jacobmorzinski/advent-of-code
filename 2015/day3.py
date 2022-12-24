#!/usr/bin/env python

# https://adventofcode.com/2015/day/3

# part1
# How many houses receive at least one present?

# part2
# Next year, how many houses receive at least one present?


import argparse
import sys
import unittest
from collections import defaultdict
from itertools import cycle


## python -m unittest day3
class TestInputs(unittest.TestCase):
    """
    > delivers presents to 2 houses: one at the starting location, and one to the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_part1(self):
        count = count_houses_visited(">")
        self.assertEqual(count, 2)
        count = count_houses_visited("^>v<")
        self.assertEqual(count, 4)
        count = count_houses_visited("^v^v^v^v^v")
        self.assertEqual(count, 2)

    def test_part2(self):
        count = count_houses_visited("^v", 2)
        self.assertEqual(count, 3)
        count = count_houses_visited("^>v<", 2)
        self.assertEqual(count, 3)
        count = count_houses_visited("^v^v^v^v^v", 2)
        self.assertEqual(count, 11)


def visit_house(houses, xy):
    visits = houses.get(xy, 0)
    houses[xy] = visits + 1

def next_address(xy, direction):
    x,y = xy
    if direction == "^":
        y += 1
    elif direction == "v":
        y -= 1
    elif direction == ">":
        x += 1
    elif direction == "<":
        x -= 1
    return (x,y)


def count_houses_visited(directions, num_santas=1):
    """Given directions to the north (^), south (v), east (>), or west (<),
    count how many houses are visited.

    Pass num_santas=2 if there is a Robo-Santa"""

    houses = {}
    xy_s = []
    santas = []
    for s in range(num_santas):
        santas.append(s)
        xy = (0,0)
        visit_house(houses, xy)
        xy_s.append(xy)

    dirs_and_santas = zip(directions, cycle(santas))

    for d_s in dirs_and_santas:
        direction = d_s[0]
        santa = d_s[1]
        xy_s[santa] = next_address(xy_s[santa], direction)
        visit_house(houses, xy_s[santa])

    # print(houses, file=sys.stderr)
    return(len(houses))


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    with open(args.input, "r") as f:
        for line in f:
            line = line.strip()
            directions = line
            c = count_houses_visited(directions)
            print(f"{c} houses visited in year 1")
            c2 = count_houses_visited(directions, 2)
            print(f"{c2} houses visited in year 2")



if __name__ == "__main__":
    sys.exit(main())

