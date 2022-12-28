#!/usr/bin/env python

# https://adventofcode.com/2015/day/13

# part1
# What is the total change in happiness for the optimal seating arrangement

# part2
# includes yourself


import argparse
import sys
import unittest
import re
import itertools


## python -m unittest day13
class TestInputs(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_input(self):
        line = 'Alice would gain 54 happiness units by sitting next to Bob.'
        self.assertEqual(parse_input(line), ('Alice', 54, 'Bob'))
        line = 'Alice would lose 79 happiness units by sitting next to Carol.'
        self.assertEqual(parse_input(line), ('Alice', -79, 'Carol'))

    def test_part1(self):
        with open("day13.input.example", "r") as f:
            people_and_neighbors = input_to_happiness(f)
            self.assertEqual(people_and_neighbors["Alice"], {'Bob': 54, 'Carol': -79, 'David': -2})
        happy, arrangement = try_permutations(people_and_neighbors)
        self.assertEqual(happy, 330)

    def test_part2(self):
        pass


def parse_input(line):
    m = re.match(r'^(?P<person>\w+) would (?P<dir>gain|lose) (?P<happiness>\d+) happiness units by sitting next to (?P<neighbor>\w+).', line)
    if m:
        person = m.group("person")
        happiness = int(m.group("happiness"))
        neighbor = m.group("neighbor")
        dir = m.group("dir")
        if dir == "lose":
            happiness = -happiness
        return (person, happiness, neighbor)


def input_to_happiness(input_stream):
    people_and_neighbors = {}
    for line in input_stream:
        person, happiness, neighbor = parse_input(line.strip())
        if person not in people_and_neighbors:
            people_and_neighbors[person] = {}
        people_and_neighbors[person][neighbor] = happiness
    # print(people_and_neighbors)
    return people_and_neighbors


def try_permutations(people_and_neighbors):
    people = list(people_and_neighbors.keys())
    # The table is cyclical.  we can anchor one person, and permute the rest.
    choices = itertools.permutations(people[1:])
    arrangements = []
    happiness = {}
    for c in choices:
        arrangement = tuple([people[0]]) + c
        arrangements.append(arrangement)
        happiness[arrangement] = calculate_happiness(people_and_neighbors, arrangement)
        # print(happiness[arrangement], arrangement)

    best_happiness = 0
    best_arrangement = None
    for arrangement, happy in happiness.items():
        if happy > best_happiness:
            best_arrangement = arrangement
            best_happiness = happy
    return best_happiness, best_arrangement


def calculate_happiness(people_and_neighbors, arrangement):
    happiness = 0
    n_guests = len(arrangement)
    for i, person in enumerate(arrangement):
        neighbor_forward = (n_guests + i + 1) % n_guests
        neighbor_backward = (n_guests + i - 1) % n_guests
        happiness += people_and_neighbors[person][arrangement[neighbor_forward]]
        happiness += people_and_neighbors[person][arrangement[neighbor_backward]]
    return happiness


def part1(input_stream):
    people_and_neighbors = input_to_happiness(input_stream)
    happy, arrangement = try_permutations(people_and_neighbors)
    # print(happy)
    # print(arrangement)
    return happy


def part2(input_stream):
    people_and_neighbors = input_to_happiness(input_stream)

    ME = "me"

    people_and_neighbors[ME] = {}
    for person, neighbors_and_happiness in people_and_neighbors.items():
        people_and_neighbors[person][ME] = 0
        for neighbor, happiness in neighbors_and_happiness.items():
            people_and_neighbors[ME][neighbor] = 0
            people_and_neighbors[neighbor][ME] = 0

    happy, arrangement = try_permutations(people_and_neighbors)
    # print(happy)
    # print(arrangement)
    return happy


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        result = part1(f)
    print(f"part 1: the happiness is {result}")

    with open(args.input, "r") as f:
        result = part2(f)
    print(f"part 2: the happiness including me is {result}")


if __name__ == "__main__":
    sys.exit(main())

