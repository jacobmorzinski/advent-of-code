#!/usr/bin/env python

# https://adventofcode.com/2015/day/9

# part1
# What is the distance of the shortest route?

# part2
# What is the distance of the longest route?


import argparse
import sys
import unittest
import re
import itertools
import copy


# https://www.math.cmu.edu/~bkell/21257-2014f/tsp.pdf
# https://www.math.cmu.edu/~bkell/21257-2014f/activity28.pdf
#
#        || to 1 | to 2 | to 3 | to 4
# ======================================
# from 1 ||   M  |  15  |  22  |  18
# from 2 ||   9  |   M  |  11  |  14
# from 3 ||  12  |  17  |   M  |  20
# from 4 ||  14  |   8  |   7  |   M
#





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


def bab_process_node(node):
    l_value = node["incoming_l_value"]

    matrix = node["incoming_matrix"]

    print(l_value)
    print(matrix)

    # matrix[city_from][city_to]
    # matrix[row][column]

    # Ensure that every row and every column has exactly one M
    cities = list(matrix.keys())
    for c1 in cities:
        count_row_m = 0
        count_col_m = 0
        for c2 in cities:
            if matrix[c1][c2] == "M":
                count_row_m += 1
            if matrix[c2][c1] == "M":
                count_col_m +=1
        if count_row_m == 0:
            matrix[c1][c2] = "M"
        if count_col_m == 0:
            matrix[c2][c1] = "M"

    # Ensure that every column contains at least one zero
    for row in cities:
        smallest_number = None
        count_zero = 0
        for col in cities:
            val = matrix[row][col]
            if isinstance(val, int):
                smallest_number = min(val,
                                      smallest_number if isinstance(smallest_number, int) else val)
            if val == 0:
                count_zero += 1
        if count_zero == 0:
            for col in cities:
                if isinstance(matrix[row][col], int):
                    matrix[row][col] -= smallest_number
            l_value += smallest_number

    # Ensure that every row contains at least one zero
    for col in cities:
        smallest_number = None
        count_zero = 0
        for row in cities:
            val = matrix[col][row]
            if isinstance(val, int):
                smallest_number = min(val,
                                      smallest_number if isinstance(smallest_number, int) else val)
            if val == 0:
                count_zero += 1
        if count_zero == 0:
            for row in cities:
                if isinstance(matrix[col][row], int):
                    matrix[col][row] -= smallest_number
            l_value += smallest_number

    # matrix is now this node's opportunity_matrix

    print(l_value)
    print(matrix)

    # special case: is the matrix 2x2
    # no it isn't
    # special case: is the only number a 0
    # no
    # ... I'm not sure I want to keep implementing this.
    

def branch_and_bound(matrix):

    node_list = []

    # Initialize root node:
    root_node = {
        "node_number": 0,
        "label": None,
        "bound": 0,
        "incoming_matrix": matrix,
        "incoming_l_value": 0,
        "opportunity_matrix": {},
        "opportunity_l_value": 0,
    }

    node_list.append(root_node)

    # Steps to process a node:
    # 1. compute the opportunity matrix and l-value
    # 2. handle special cases
    # 4. calculate and handle regrets
    # 6. create and recurse into child nodes

    bab_process_node(root_node)
    
    pass

    
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
    count = 0
    for t in tries:
        count += 1
        distance = calculate_distance(city_graph, t)
        # print(distance, t)
        min_distance = min(distance, min_distance or distance)

    print(f"tested {count} paths")
    return min_distance


    # # Branch and Bound
    # distance_matrix = copy.deepcopy(city_graph)
    # for city in cities:
    #     distance_matrix[city][city] = "M"
    # min_distance = branch_and_bound(distance_matrix)
    # return min_distance


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

    with open(args.input, "r") as f:
        total = part1(f)
    print(f"part 1: the minimum path is {total}")

    with open(args.input, "r") as f:
        total = part2(f)
    print(f"part 2: the maximum path is {total}")



if __name__ == "__main__":
    sys.exit(main())

