#!/usr/bin/env python

# https://adventofcode.com/2015/day/15

# part1
# what is the total score of the highest-scoring cookie you can make?

# part2
# ...with a calorie total of 500?


import argparse
import sys
import unittest
import re
import random
import copy


## python -m unittest day15
class TestInputs(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_input(self):
        line = 'Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8'
        self.assertEqual(parse_input(line), {'Butterscotch': (-1, -2, 6, 3, 8)})
        line = 'Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'
        self.assertEqual(parse_input(line), {'Cinnamon': (2, 3, -2, -1, 3)})

    def test_compute_cookie_score(self):
        ingredient_properties = {
            'Butterscotch': (-1, -2, 6, 3, 8),
            'Cinnamon': (2, 3, -2, -1, 3),
        }
        cookie = {
            'Butterscotch': 44,
            'Cinnamon': 56,
        }
        score, calories = compute_cookie_score(cookie, ingredient_properties)
        self.assertEqual(score, 62842880)

    def test_part1(self):
        pass

    def test_part2(self):
        pass


def parse_input(line):
    m = re.match(r'^(?P<ingredient>\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line)
    if m:
        ingredient = m.group(1)
        capacity = int(m.group(2))
        durability = int(m.group(3))
        flavor = int(m.group(4))
        texture = int(m.group(5))
        calories = int(m.group(6))

        return {ingredient: (capacity, durability, flavor, texture, calories)}


def compute_cookie_score(cookie, ingredient_properties):

    # i1 units of ingredient 1
    # i2 units of ingredient 2
    # i3 units of ingredient 3
    # i4 units of ingredient 4

    # net_capacity = i1 * capacity + i2 * capacity + i3 * capacity + i3 * capacity
    # net_durability = i1 * durability + i2 * durability + i3 * durability + i3 * durability
    # net_flavor = i1 * flavor + i2 * flavor + i3 * flavor + i3 * flavor
    # net_texture = i1 * texture + i2 * texture + i3 * texture + i3 * texture

    # note: if any net_* component is negative, set it to 0

    # total_score = net_capacity * net_durability * net_flavor * net_texture

    # net_calories = i1 * calories + i2 * calories + i3 * calories + i3 * calories

    net_capacity = 0
    net_durability = 0
    net_flavor = 0
    net_texture = 0
    net_calories = 0
    for ingredient, amount in cookie.items():
        (capacity, durability, flavor, texture, calories) = ingredient_properties[ingredient]
        net_capacity += amount * capacity
        net_durability += amount * durability
        net_flavor += amount * flavor
        net_texture += amount * texture
        net_calories += amount * calories

    net_capacity = max(0, net_capacity)
    net_durability = max(0, net_durability)
    net_flavor = max(0, net_flavor)
    net_texture = max(0, net_texture)

    return net_capacity * net_durability * net_flavor * net_texture, net_calories


def make_random_cookie(ingredients):
    cookie = {
        'Sprinkles': 0,
        'Butterscotch': 0,
        'Chocolate': 0,
        'Candy': 0
    }
    remaining = 100
    ingredients = list(ingredients)
    random.shuffle(ingredients)
    for n,i in enumerate(ingredients):
        cookie[i] = random.randint(0, remaining)
        remaining -= cookie[i]
        if n+1 == len(ingredients):
            cookie[i] += remaining

    cookie = {
        'Sprinkles': 28,
        'Butterscotch': 28,
        'Chocolate': 35,
        'Candy': 9,
    }

    # hand-choose a cookie that is already a 500-calorie cookie
    cookie = {'Sprinkles': 32, 'Butterscotch': 28, 'Chocolate': 32, 'Candy': 8}
    return cookie


def iterate_cookie(cookie, ingredient_properties, calorie_limit=None):
    new_cookie = copy.deepcopy(cookie)


    if calorie_limit is None:
        ingredients = sorted(new_cookie.keys())
        up, down = random.sample(ingredients, 2)
        if (new_cookie[up] < 100) and (new_cookie[down] > 0):
            new_cookie[up] += 1
            new_cookie[down] -= 1
    else:
        # ingredients = ('Sprinkles', 'Butterscotch', 'Chocolate', 'Candy')
        up_down_choices = [
            ('Sprinkles', 'Chocolate'),
            ('Sprinkles', 'Candy'),
            ('Sprinkles', 'Chocolate'),
            ('Sprinkles', 'Chocolate'),
        ]

    return new_cookie


def find_best_cookie(ingredient_properties, calorie_limit=None):

    # constraint: i1 + i2 + i3 + i4 = 100
    # constraint: sum(i_n * calories_n) = calorie_limit (like 500)

    # i_s = 100, 0, 0, 0
    # i_s = 99, 1, 0, 0,
    #    or 99, 0, 1, 0,
    #    or 99, 0, 0, 1
    # i_s = 98, 2, 0, 0,
    #    or 98, 0, 2, 0,
    #    or 98, 0, 0, 2,
    #    or 98, 1, 1, 0,
    #    or 98, 1, 0, 1,
    #    or 98, 0, 1, 1,
    # enumeration seems expensive

    # Can we walk to a solution?  The negatives mean the final answer
    # isn't linear, but intermediate equations are linear and maybe we
    # can avoid the boundaries where things go negative.

    ingredients = ('Sprinkles', 'Butterscotch', 'Chocolate', 'Candy')

    count_found = 0
    for _ in range(100):
        cookie = make_random_cookie(ingredients)
        score, calories = compute_cookie_score(cookie, ingredient_properties)
        if score > 0:
            # print(score, cookie)
            count_found += 1
            if count_found >= 1:
                break

    max_score = score
    for _ in range(100_000):
        new_cookie = iterate_cookie(cookie, ingredient_properties)
        new_score, new_calories = compute_cookie_score(new_cookie, ingredient_properties)
        if (calorie_limit and new_calories != calorie_limit
            and abs(new_calories - calories) > 0):
            # force calories to converge
            # ...no this doens't force convergence,
            # because we only save cookies when the score improves.
            # TODO: change to a multi-phase algorithm.
            continue
        if new_score > max_score:
            max_score = new_score
            cookie = new_cookie
            # print(new_score, new_calories, new_cookie)
    print(max_score, cookie)
    return max_score


def part1(input_stream):
    ingredient_properties = {}
    for line in input_stream:
        ingredient_properties.update(parse_input(line.strip()))

    score = find_best_cookie(ingredient_properties)
    return score


def part2(input_stream):
    ingredient_properties = {}
    for line in input_stream:
        ingredient_properties.update(parse_input(line.strip()))

    score = find_best_cookie(ingredient_properties, calorie_limit=500)
    return score

def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        result = part1(f)
    print(f"part 1: the cookie score is {result}")

    with open(args.input, "r") as f:
        result = part2(f)
    print(f"part 2: the cookie score of a 500-calorie cookie is {result}")


if __name__ == "__main__":
    sys.exit(main())

