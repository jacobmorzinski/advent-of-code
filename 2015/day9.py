#!/usr/bin/env python

# https://adventofcode.com/2015/day/9

# part1
# What is the distance of the shortest route?

# part2
# 


import argparse
import sys
import unittest
import re
import itertools


## python -m unittest day9
class TestInputs(unittest.TestCase):
    """

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_part1(self):
        pass


    def test_part2(self):
        pass


def parse_input(line):
    m = re.match(r'^(?P<city1>\w+) to (?P<city2>\w+) = (?P<distance>\d+)$', line)
    if m:
        return m.groups()


def calculate_distance(city_graph, path):
    """Given a path, calculate the distance through the city graph"""

    distance = 0
    current_city = path[0]
    for next_city in path[1:]:
        distance += city_graph[current_city][next_city]
        current_city = next_city

    return distance

def part1(input_stream):
    """Read city distances and calculate a minimum path
    """

    total = 0
    city_graph = {}
    for line in input_stream:
        city1, city2, distance = parse_input(line.strip())
        distance = int(distance)
        if not city1 in city_graph:
            city_graph[city1] = {}
        city_graph[city1].update({city2: distance})
        if not city2 in city_graph:
            city_graph[city2] = {}
        city_graph[city2].update({city1: distance})

    cities = set(city_graph.keys())

    min_distance = None

    # 40320 permutations
    tries = list(itertools.permutations(cities))
    for t in tries:
        distance = calculate_distance(city_graph, t)
        # print(distance, t)
        min_distance = min(distance, min_distance or distance)
    
    return min_distance


def part2(input_stream):
    """Read city distances and calculate a longest path
    """

    total = 0
    city_graph = {}
    for line in input_stream:
        city1, city2, distance = parse_input(line.strip())
        distance = int(distance)
        if not city1 in city_graph:
            city_graph[city1] = {}
        city_graph[city1].update({city2: distance})
        if not city2 in city_graph:
            city_graph[city2] = {}
        city_graph[city2].update({city1: distance})

    cities = set(city_graph.keys())

    max_distance = None

    # 40320 permutations
    tries = list(itertools.permutations(cities))
    for t in tries:
        distance = calculate_distance(city_graph, t)
        # print(distance, t)
        max_distance = max(distance, max_distance or distance)
    
    return max_distance


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    count_nice_strings = 0
    count_nice_strings_v2 = 0

    with open(args.input, "r") as f:
        total = part1(f)
    print(f"part 1: the minimum path is {total}")

    with open(args.input, "r") as f:
        total = part2(f)
    print(f"part 2: the maximum path is {total}")



if __name__ == "__main__":
    sys.exit(main())

