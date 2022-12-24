#!/usr/bin/env python

# https://adventofcode.com/2015/day/7

# part1
# what signal is ultimately provided to wire a?

# part2
# 


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

        instructions = {}
        wires = {}

        for line in input_stream:
            tokens = shlex.split(line.strip())
            wire = tokens[-1]
            wires[wire] = tokens[:-2]

        for wire, expr in wires.items():
            if (isinstance(expr, list)
                and len(expr) == 1):
                arg1 = expr[0]
                val = int(arg1)
                wires[wire] = val
            elif (isinstance(expr, list)
                  and len(expr) == 2):
                op = expr[0]
                arg1 = expr[1]
                if (isinstance(wires[arg1], int)
                    and op == 'NOT'):
                    val = (~ wires[arg1]) & 65535
                    wires[wire] = val
            elif (isinstance(expr, list)
                  and len(expr) == 3):
                op = expr[1]
                if op == 'AND':
                    arg1 = expr[0]
                    arg2 = expr[2]
                    if (isinstance(wires[arg1], int)
                        and isinstance(wires[arg2], int)):
                        val = wires[arg1] & wires[arg2]
                        wires[wire] = val
                if op == 'OR':
                    arg1 = expr[0]
                    arg2 = expr[2]
                    if (isinstance(wires[arg1], int)
                        and isinstance(wires[arg2], int)):
                        val = wires[arg1] | wires[arg2]
                        wires[wire] = val
                if op == 'LSHIFT':
                    arg1 = expr[0]
                    arg2 = expr[2]
                    if (isinstance(wires[arg1], int)):
                        val = (wires[arg1] << int(arg2)) & 65535
                        wires[wire] = val
                if op == 'RSHIFT':
                    arg1 = expr[0]
                    arg2 = expr[2]
                    if (isinstance(wires[arg1], int)):
                        val = (wires[arg1] >> int(arg2)) & 65535
                        wires[wire] = val

                
                
        print(wires)
        # self.assertEqual(inputs, "")

        for wire,expected_value in expected_results.items():
            with self.subTest(wire=wire, expected_value=expected_value):
                self.assertEqual(expected_value, wires[wire])




    def test_part2(self):
        pass


        
def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    count_nice_strings = 0
    count_nice_strings_v2 = 0
    with open(args.input, "r") as f:
        for line in f:
            line = line.strip()
            puzzle_input = line
            result = is_string_nice(puzzle_input)
            if result == "nice":
                count_nice_strings += 1
            result_v2 = is_string_nice_v2(puzzle_input)
            if result_v2 == "nice":
                count_nice_strings_v2 += 1
            

    print(f"{count_nice_strings} strings are nice")
    print(f"{count_nice_strings_v2} strings are nice v2")

if __name__ == "__main__":
    sys.exit(main())

