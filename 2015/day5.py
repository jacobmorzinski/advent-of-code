#!/usr/bin/env python

# https://adventofcode.com/2015/day/5

# part1
# How many strings are nice?

# part2
# How many strings are nice under these new rules?


import argparse
import sys
import unittest


## python -m unittest day5
class TestInputs(unittest.TestCase):
    """

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_part1(self):
        inputs_outputs = [ ("ugknbfddgicrmopn", "nice"),
                           ("aaa", "nice"),
                           ("jchzalrnumimnmhp", "naughty"),
                           ("haegwjzuvuyypxyu", "naughty"),
                           ("dvszwmarrgswjxmb", "naughty")]

        for in_out in inputs_outputs:
            with self.subTest(in_out=in_out):
                puzzle_input, expected_result = in_out
                result = is_string_nice(puzzle_input)
                self.assertEqual(result, expected_result)


    def test_part2(self):
        inputs_outputs = [ ("qjhvhtzxzqqjkmpb", "nice"),
                           ("xxyxx", "nice"),
                           ("uurcxstgmygtbstg", "naughty"),
                           ("ieodomkazucvgmuy", "naughty")]

        for in_out in inputs_outputs:
            with self.subTest(in_out=in_out):
                puzzle_input, expected_result = in_out
                result = is_string_nice_v2(puzzle_input)
                self.assertEqual(result, expected_result)


def is_string_nice(s):
    """
    A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
    """

    vowels = "aeiou"
    unwanted = ["ab", "cd", "pq", "xy"]

    for u in unwanted:
        if u in s:
            return "naughty"

    prev_c = ""
    twice_in_a_row = False
    seen_vowels = 0
    for c in s:
        if (not twice_in_a_row) and (c == prev_c):
            twice_in_a_row = True
        if c in vowels:
            seen_vowels += 1
        prev_c = c

    if twice_in_a_row and seen_vowels >= 3:
        return "nice"

    return "naughty"


def is_string_nice_v2(s):
    """
    A nice string is one with all of the following properties:

    It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
    """

    repeat_seen = False
    pair_seen = False
    pairs_found = {}
    ring_buffer = ["","","",""]
    for c in s:
        ring_buffer.pop(0)
        ring_buffer.append(c)
        if ((ring_buffer[-1] == ring_buffer[-2])
            and (ring_buffer[-2] == ring_buffer[-3])
            and (ring_buffer[-3] != ring_buffer[-4])):
            pass                # disallow 3-char overlap, allow 4-char overlap
        else:
            k = tuple(ring_buffer[-2:])
            pairs_found[k] = pairs_found.get(k,0) + 1
            if pairs_found[k] > 1:
                pair_seen = True
        if (ring_buffer[-1] == ring_buffer[-3]):
            repeat_seen = True
        if pair_seen and repeat_seen:
            return "nice"

    return "naughty"

        
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

