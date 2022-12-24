#!/usr/bin/env python

# https://adventofcode.com/2015/day/1
# To what floor do the instructions take Santa?

# part2
# What is the position of the character that causes Santa to first enter the basement?

import argparse
import sys

def find_final_floor(input):
    floor=0
    seen_basement=False
    position=0
    with open(input, "r") as f:
        while True:
            c = f.read(1)
            if floor < 0:
                seen_basement = True
            if not seen_basement:
                position += 1
            if c == "(":
                floor += 1
            elif c == ")":
                floor -= 1
            elif c == "":
                break
    return floor, position

def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    floor, position = find_final_floor(args.input)
    print(f"Floor is {floor}")
    print(f"Seen basement at position {position}")

if __name__ == "__main__":
    sys.exit(main())

