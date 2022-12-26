#!/usr/bin/env python

# https://adventofcode.com/2015/day/11

# part1
# what should [Santa's] next password be?

# part2
# Santa's password expired again. What's the next one?


import argparse
import sys
import unittest
import re


## python -m unittest day11
class TestInputs(unittest.TestCase):
    """

    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pw_policy_straight(self):
        "Passwords must include one increasing straight of at least three letters."

        self.assertEqual(pw_policy_straight("hijklmmn"), True)
        self.assertEqual(pw_policy_straight("abbceffg"), False)

    def test_pw_policy_iol(self):
        "Passwords may not contain the letters i, o, or l."

        self.assertEqual(pw_policy_iol("hijklmmn"), False)

    def test_pw_policy_pairs(self):
        "Passwords must contain at least two different, non-overlapping pairs of letters."

        self.assertEqual(pw_policy_pairs("abbceffg"), True)
        self.assertEqual(pw_policy_pairs("abbcegjk"), False)

    def test_find_next_password_1(self):
        "The next password after abcdefgh is abcdffaa."

        self.assertEqual(find_next_password("abcdefgh"), "abcdffaa")

    def test_find_next_password_2(self):
        "The next password after ghijklmn is ghjaabcc"

        self.assertEqual(find_next_password("ghijklmn"), "ghjaabcc")

    def test_part1(self):
        pass

    def test_part2(self):
        pass


def pw_policy_straight(s):
    "Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count."

    last3 = [" "," "," "]    # arbitrary starting characters
    straight_seen = False
    for c in s:
        last3.pop(0)
        last3.append(c)
        if ((ord(last3[2]) - ord(last3[1])) == 1
            and (ord(last3[1]) - ord(last3[0])) == 1):
            straight_seen = True
            break
    return straight_seen
        

def pw_policy_iol(s):
    "Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing."

    m = re.search(r'[iol]', s)
    if m:
        return False
    else:
        return True
    

def pw_policy_pairs(s):
    "Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz."

    pairs = {}
    history = [" ", " ", " "]
    for c in s:
        if (c == history[-1]
            and ((c == history[-2] and c == history[-3])
                 or c != history[-2])):
            pairs[c] = pairs.get(c, 0) + 1
        history.pop(0)
        history.append(c)

    if len(pairs) > 1:
        return True
    else:
        return False
                

def increment_password(s):
    r = reversed([c for c in s])
    ans = []
    carry = 0
    arg0 = 1
    for c in r:
        c = chr(ord(c) + arg0 + carry)
        arg0 = 0
        if c > "z":
            c = "a"
            carry = 1
        else:
            carry = 0
        ans.append(c)
    if carry == 1:
        ans.append("a")

    return("".join(reversed(ans)))


def find_next_password(pw):
    """Incrementing is just like counting with numbers: xx, xy, xz,
    ya, yb, and so on. Increase the rightmost letter one step; if it
    was z, it wraps around to a, and repeat with the next letter to
    the left until one doesn't wrap around."""

    new_pw = increment_password(pw)
    satisfies_pw_policy = False
    for _ in range(10_000_000):
        satisfies_pw_policy = (pw_policy_straight(new_pw)
                               and pw_policy_iol(new_pw)
                               and pw_policy_pairs(new_pw))
        if satisfies_pw_policy:
            return new_pw
        else:
            new_pw = increment_password(new_pw)
    raise(Exception("too many loops in find_next_password"))


def part1(input_stream):
    """
    """

    for line in input_stream:
        pw = line.strip()
        next_pw = find_next_password(pw)

    return next_pw


def part2(input_stream):
    """
    """

    for line in input_stream:
        pw = line.strip()
        next_pw = find_next_password(pw)
        next_pw = find_next_password(next_pw)

    return next_pw


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)

    args = parser.parse_args()

    with open(args.input, "r") as f:
        result = part1(f)
    print(f"part 1: the next password is {result}")

    with open(args.input, "r") as f:
        result = part2(f)
    print(f"part 2: the next again password is {result}")



if __name__ == "__main__":
    sys.exit(main())

