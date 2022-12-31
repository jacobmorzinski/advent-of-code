#!/usr/bin/env python

# https://adventofcode.com/2015/day/14

# part1
# after exactly 2503 seconds, what distance has the winning reindeer traveled?

# part2
# with the new scoring system, how many points does the winning reindeer have?


import argparse
import sys
import unittest
import re


## python -m unittest day14
class TestInputs(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_input(self):
        line = 'Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.'
        self.assertEqual(parse_input(line), ('Comet', 14, 10, 127) )
        line = 'Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'
        self.assertEqual(parse_input(line), ('Dancer', 16, 11, 162))

    def test_compute_reindeer_distance(self):
        reindeer_description = ('Comet', 14, 10, 127)
        distance = compute_reindeer_distance(reindeer_description, 1000)
        self.assertEqual(distance, 1120)

        reindeer_description = ('Dancer', 16, 11, 162)
        distance = compute_reindeer_distance(reindeer_description, 1000)
        self.assertEqual(distance, 1056)

    def test_compute_reindeer_points(self):
        reindeers = [
            ('Comet', 14, 10, 127),
            ('Dancer', 16, 11, 162),
        ]
        points = compute_reindeer_points(reindeers, 1000)
        self.assertEqual(points, [('Comet', 312), ('Dancer', 689)])
        pass

    def test_part1(self):
        pass

    def test_part2(self):
        pass


def parse_input(line):
    m = re.match(r'^(?P<reindeer>\w+) can fly (?P<speed_kms>\d+) km/s for (?P<fly_time_s>\d+) seconds, but then must rest for (?P<rest_time_s>\d+) seconds.', line)
    if m:
        reindeer = m.group('reindeer')
        speed_kms = int(m.group('speed_kms'))
        fly_time_s = int(m.group('fly_time_s'))
        rest_time_s = int(m.group('rest_time_s'))
        return reindeer, speed_kms, fly_time_s, rest_time_s


def compute_reindeer_distance(reindeer_description, time_s):
    "Given a reindeer description and a time (in seconds), compute the distance traveled"
    name = reindeer_description[0]
    speed_kms = reindeer_description[1]
    fly_time_s = reindeer_description[2]
    rest_time_s = reindeer_description[3]

    time_remaining_s = time_s
    distance_km = 0
    while time_remaining_s > 0:
        flight_phase_s = min(time_remaining_s, fly_time_s)
        time_remaining_s -= flight_phase_s
        distance_km += flight_phase_s * speed_kms

        rest_phase_s = min(time_remaining_s, rest_time_s)
        time_remaining_s -= rest_phase_s

    return distance_km


def compute_reindeer_points(reindeers, time_s):
    "Given a list of all reindeers and a time (in seconds), compute the points earned"

    state = {}
    for reindeer in reindeers:
        name = reindeer[0]
        state[name] = {
            "distance_km": 0,
            "points": 0,
        }

    max_distance_km = 0
    for s in range(1,time_s+1):
        for reindeer in reindeers:
            name = reindeer[0]
            distance_km = compute_reindeer_distance(reindeer, s)
            state[name]["distance_km"] = distance_km
        max_distance_km = max([state[r[0]]["distance_km"] for r in reindeers])
        fastest_reindeer = set()
        for reindeer in reindeers:
            if state[reindeer[0]]["distance_km"] == max_distance_km:
                fastest_reindeer.add(reindeer[0])
                state[reindeer[0]]["points"] += 1
        # print(max_distance_km, fastest_reindeer)

    return [(k, state[k]["points"]) for k in state]


def part1(input_stream):
    max_distance_km = 0
    fastest_reindeer = None
    race_time_s = 2503
    for line in input_stream:
        reindeer_description = parse_input(line.strip())
        distance_km = compute_reindeer_distance(reindeer_description, race_time_s)
        if distance_km > max_distance_km:
            max_distance_km = distance_km
            fastest_reindeer = reindeer_description[0]
    print(fastest_reindeer, max_distance_km)
    return max_distance_km


def part2(input_stream):
    max_points = 0
    fastest_reindeer = None
    race_time_s = 2503

    reindeers = []
    for line in input_stream:
        reindeer_description = parse_input(line.strip())
        reindeers.append(reindeer_description)

    points = compute_reindeer_points(reindeers, race_time_s)
    for r in points:
        name = r[0]
        points = r[1]
        if points >= max_points:
            fastest_reindeer = name
            max_points = points

    return max_points


def main():
    parser = argparse.ArgumentParser(description='Advent of Code.')
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input, "r") as f:
        result = part1(f)
    print(f"part 1: the winning reindeer travelled {result}")

    with open(args.input, "r") as f:
        result = part2(f)
    print(f"part 2: the winning reindeer has {result} points")


if __name__ == "__main__":
    sys.exit(main())

