#!/usr/bin/env python

# https://adventofcode.com/2015/day/16

# part1
# What is the number of the Sue that got you the gift?

# part2
# What is the number of the real Aunt Sue?


import argparse
import sys
import unittest
import re
import io
import copy
import operator


MFCSAM_INPUT = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""


## python -m unittest day16
class TestInputs(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_input(self):
        line = 'Sue 1: children: 1, cars: 8, vizslas: 7'
        self.assertEqual(parse_input(line), {1: {'cars': '8', 'children': '1', 'vizslas': '7'}})

    def test_part1(self):
        pass

    def test_part2(self):
        pass


def parse_input(line):
    m = re.match(r'^Sue (?P<number>\d+): ', line)
    if m:
        sue_number = int(m.group(1))
    else:
        raise Exception('No sue number in: "f{line}"')

    attribute_text = re.sub(r'^Sue (?P<number>\d+): ', '', line)
    attributes = attribute_text.split(", ")
    attributes = map(lambda x: x.split(": "), attributes)
    attributes = dict(attributes)

    sue = {sue_number: attributes}

    return sue


def part1(input_stream):

    desired_sue = {}
    for line in io.StringIO(MFCSAM_INPUT):
        desired_sue.update(dict([(line.strip()).split(": ")]))


    sues = {}
    for line in input_stream:
        sues.update(parse_input(line.strip()))

    candidates = copy.deepcopy(sues)
    for sue,detections in sues.items():
        wrong_sue = False
        for d, n in detections.items():
            if desired_sue[d] == n:
                pass
            else:
                wrong_sue = True
        if wrong_sue:
            del(candidates[sue])

    return list(candidates.keys())


def part2(input_stream):

    desired_sue = {}
    for line in io.StringIO(MFCSAM_INPUT):
        desired_sue.update(dict([(line.strip()).split(": ")]))

    sues = {}
    for line in input_stream:
        sues.update(parse_input(line.strip()))

    candidates = copy.deepcopy(sues)
    for sue,detections in sues.items():
        wrong_sue = False
        for d, n in detections.items():
            # cats and trees readings indicates that there are greater than that many
            # pomeranians and goldfish readings indicate that there are fewer than that many
            if d in ("cats", "trees"):
                op = operator.gt
            elif d in ("pomeranians", "goldfish"):
                op = operator.lt
            else:
                op = operator.eq

            if op(n, desired_sue[d]):
                pass
            else:
                wrong_sue = True
        if wrong_sue:
            del(candidates[sue])

    return list(candidates.keys())


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        result = part1(f)
    print(f"part 1: the gift is from Aunt Sue number {result}")

    with open(args.input, "r") as f:
        result = part2(f)
    print(f"part 2: adjusting for retroencabulator, the gift is from Aunt Sue number {result}")


if __name__ == "__main__":
    sys.exit(main())

