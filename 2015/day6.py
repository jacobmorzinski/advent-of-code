#!/usr/bin/env python

# https://adventofcode.com/2015/day/6

# part1
# After following the instructions, how many lights are lit?

# part2
# What is the total brightness of all lights combined after following Santa's instructions?


import argparse
import sys
import unittest
import shlex


## python -m unittest day6
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


def part1(input_stream):
    """
    turn on 0,0 through 999,999 would turn on (or leave on) every light.
    toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning off the ones that were on, and turning on the ones that were off.
    turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.
    """

    lights = [[]] * 1000
    for y in range(0,1000):
        lights[y] = [False] * 1000

    for line in input_stream:
        instruction = line.strip()
        tokens = shlex.split(instruction)
        if tokens[0] == "turn":
            tokens.pop(0)
        lower_left = tokens[1]
        ll = list(map(int, lower_left.split(',')))
        upper_right = tokens[3]
        ur = list(map(int, upper_right.split(',')))

        for y in range(ll[1], 1+ur[1]):
            for x in range(ll[0], 1+ur[0]):
                if tokens[0] == "on":
                    lights[x][y] = True
                elif tokens[0] == "off":
                    lights[x][y] = False
                if tokens[0] == "toggle":
                    lights[x][y] = not lights[x][y]


        count_on = 0
        for y in range(0,1000):
            for x in range(0,1000):
                if lights[x][y]:
                    count_on += 1

    return count_on


def part2(input_stream):
    """
    The phrase turn on actually means that you should increase the brightness of those lights by 1.
    The phrase turn off actually means that you should decrease the brightness of those lights by 1, to a minimum of zero.
    The phrase toggle actually means that you should increase the brightness of those lights by 2.
    """

    lights = [[]] * 1000
    for y in range(0,1000):
        lights[y] = [0] * 1000

    for line in input_stream:
        instruction = line.strip()
        tokens = shlex.split(instruction)
        if tokens[0] == "turn":
            tokens.pop(0)
        lower_left = tokens[1]
        ll = list(map(int, lower_left.split(',')))
        upper_right = tokens[3]
        ur = list(map(int, upper_right.split(',')))

        for y in range(ll[1], 1+ur[1]):
            for x in range(ll[0], 1+ur[0]):
                if tokens[0] == "on":
                    lights[x][y] += 1
                elif tokens[0] == "off":
                    lights[x][y] = max(0, lights[x][y] - 1)
                if tokens[0] == "toggle":
                    lights[x][y] += 2


        brightness = 0
        for y in range(0,1000):
            for x in range(0,1000):
                brightness += lights[x][y]

    return brightness

        
def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    with open(args.input, "r") as f:
        count_lights = part1(f)
    print(f"{count_lights} lights are lit (part 1)")

    with open(args.input, "r") as f:
        brightness = part2(f)
            
    print(f"{brightness} brightness (part 2)")


if __name__ == "__main__":
    sys.exit(main())

