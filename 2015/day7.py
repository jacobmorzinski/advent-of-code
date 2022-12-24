#!/usr/bin/env python

# https://adventofcode.com/2015/day/7

# part1
# what signal is ultimately provided to wire a?

# part2
# What new signal is ultimately provided to wire a?


import argparse
import sys
import unittest
import io
import shlex


## python -m unittest day7
class TestInputs(unittest.TestCase):
    """

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_part1(self):
        """
        For example, here is a simple circuit: ...
        After it is run, these are the signals on the wires: ...
        """

        inputs = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

        input_stream = io.StringIO(inputs)

        wires = part1(input_stream)

        expected_results = {
            "d": 72,
            "e": 507,
            "f": 492,
            "g": 114,
            "h": 65412,
            "i": 65079,
            "x": 123,
            "y": 456,
        }

        for wire,expected_value in expected_results.items():
            with self.subTest(wire=wire, expected_value=expected_value):
                self.assertEqual(expected_value, wires[wire])


    def test_part2(self):
        pass


def resolve(term, wires):
    try:
        val = int(term)
        return val
    except ValueError as e:
        pass

    val = wires.get(term)
    if isinstance(val, int):
        return val

    return term


def resolve_wires(wires):
    "One resolve pass on the wires"

    ground_terms = 0
    for wire, expr in wires.items():
        # print(wire, expr)

        if isinstance(expr, int):
            ground_terms += 1

        elif (isinstance(expr, list)
            and len(expr) == 1):
            arg1 = resolve(expr[0], wires)
            if (isinstance(arg1, int)):
                wires[wire] = arg1

        elif (isinstance(expr, list)
              and len(expr) == 2):
            op = expr[0]
            arg1 = resolve(expr[1], wires)
            if (isinstance(arg1, int)
                and op == 'NOT'):
                val = (~ arg1) & 65535
                wires[wire] = val

        elif (isinstance(expr, list)
              and len(expr) == 3):

            op = expr[1]
            if op == 'AND':
                arg1 = resolve(expr[0], wires)
                arg2 = resolve(expr[2], wires)
                if (isinstance(arg1, int)
                    and isinstance(arg2, int)):
                    val = arg1 & arg2
                    wires[wire] = val
            if op == 'OR':
                arg1 = resolve(expr[0], wires)
                arg2 = resolve(expr[2], wires)
                if (isinstance(arg1, int)
                    and isinstance(arg2, int)):
                    val = arg1 | arg2
                    wires[wire] = val
            if op == 'LSHIFT':
                arg1 = resolve(expr[0], wires)
                arg2 = expr[2]
                if (isinstance(arg1, int)):
                    val = (arg1 << int(arg2)) & 65535
                    wires[wire] = val
            if op == 'RSHIFT':
                arg1 = resolve(expr[0], wires)
                arg2 = expr[2]
                if (isinstance(arg1, int)):
                    val = (arg1 >> int(arg2)) & 65535
                    wires[wire] = val

        else:
            print("unhandled expr", wire, expr)

    # print(f"{ground_terms} ground terms")

    return wires


def part1(input_stream):
    """Read instructions from the input stream
    and return wires.
    """

    wires = {}

    for line in input_stream:
        tokens = shlex.split(line.strip())
        wire = tokens[-1]
        wires[wire] = tokens[:-2]

    for _ in range(150):
        wires = resolve_wires(wires)

    return wires


def part2(input_stream, override):
    """Read instructions from the input stream,
    override b,
    and return wires.
    """

    wires = {}

    for line in input_stream:
        tokens = shlex.split(line.strip())
        wire = tokens[-1]
        wires[wire] = tokens[:-2]

    wires['b'] = override

    for _ in range(150):
        wires = resolve_wires(wires)

    return wires


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    count_nice_strings = 0
    count_nice_strings_v2 = 0

    with open(args.input, "r") as f:
        wires = part1(f)
    print(f"the signal on 'a' is {wires['a']}")

    with open(args.input, "r") as f:
        wires = part2(f, wires['a'])
    print(f"part 2: the signal on 'a' is {wires['a']}")


if __name__ == "__main__":
    sys.exit(main())

