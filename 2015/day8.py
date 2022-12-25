#!/usr/bin/env python

# https://adventofcode.com/2015/day/8

# part1
# what is the number of characters of code for string literals
# minus the number of characters in memory for the values of the
# strings in total for the entire file?

# part2
# now encode each code representation as a new string and find
# the number of characters of the new encoded representation,
# including the surrounding double quotes


import argparse
import sys
import unittest
import re


## python -m unittest day8
class TestInputs(unittest.TestCase):
    """

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_part1(self):

        # input string:
        # (characters_of_string_code, characters_in_memory)
        inputs_outputs = {
            r'""': (2, 0),
            r'"abc"': (5,3),
            r'"aaa\"aaa"': (10,7),
            r'"\x27"': (6, 1),
        }

        for s, (c, m) in inputs_outputs.items():
            with self.subTest(s=s, c=c, m=m):
                self.assertEqual(count_characters(s), (c,m))


    def test_part2(self):

        # input string:
        # (characters_of_string_code, characters_when_encoded)
        inputs_outputs = {
            r'""': (2, 6),
            r'"abc"': (5,9),
            r'"aaa\"aaa"': (10,16),
            r'"\x27"': (6, 11),
        }

        for s, (c, e) in inputs_outputs.items():
            with self.subTest(s=s, c=c, e=e):
                self.assertEqual(count_encoded(s), (c,e))


def str_unescape(m):
    g1 = m.group(1)
    if g1 == '"':
        return '"'
    elif g1 == '\\':
        return '\\'
    elif g1.startswith("x"):
        codes = m.group(2)
        ascii_val = int(codes, 16)
        return chr(ascii_val)


def unquote_unescape(s):

    # surrounding quotes
    t = re.sub(r'^"(.*?)"$', r'\g<1>', s)

    # escaped item
    t = re.sub(r'(?i)\\("|\\|x([0-9a-f]{2}))', str_unescape, t)

    return t


def count_characters(s):
    """
    s: input string
    return(c,m): (characters_of_string_code, characters_in_memory)
    """

    c = len(s)
    m = len(unquote_unescape(s))
    return c,m


def str_escape(m):
    g1 = m.group(1)
    if g1 == '"':
        return '\\"'
    elif g1 == '\\':
        return '\\\\'

    return ""


def do_quote(s):

    t = re.sub(r'("|\\)', str_escape, s)

    t = '"' + t + '"'
    return t


def count_encoded(s):
    """
    input string:
    (characters_of_string_code, characters_when_encoded)
    """

    c = len(s)
    e = len(do_quote(s))
    return c,e


def part1(input_stream):
    """Read strings and return the sum of the differences of the character counts.
    """

    total = 0
    for line in input_stream:
        c,m = count_characters(line.strip())
        total += (c - m)

    return total


def part2(input_stream):
    """Read strings and return the sum of the differences of the character counts.
    """

    total = 0
    for line in input_stream:
        c,e = count_encoded(line.strip())
        total += (e - c)

    return total


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    count_nice_strings = 0
    count_nice_strings_v2 = 0

    with open(args.input, "r") as f:
        total = part1(f)
    print(f"part 1: the sum of difference is {total}")

    with open(args.input, "r") as f:
        total = part2(f)
    print(f"part 2: the sum of difference is {total}")



if __name__ == "__main__":
    sys.exit(main())

