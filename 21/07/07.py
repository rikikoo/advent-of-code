#!/usr/bin/env python3

import sys
from statistics import median, mean


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # assuming that input is a single line of comma separated integers
            positions = list(map(int, f.readline().strip().split(',')))
    except OSError:
        print(f"Error opening file: {filename}")
        quit()

    # median
    target_pos = round(median(positions))
    fuel_consumption = sum([abs(pos - target_pos) for pos in positions])
    print(f"Sum of distances of the positions from the median: {fuel_consumption}")

    # mean
    target_pos = round(mean(positions))
    fuel_consumption = sum([sum(range(abs(pos - target_pos) + 1)) for pos in positions])

    # floored mean
    target_pos = round(mean(positions)) - 1     # decrement by 1 to effectively round down
    fuel_consumption_floor = sum([sum(range(abs(pos - target_pos) + 1)) for pos in positions])

    fuel_consumption = min(fuel_consumption, fuel_consumption_floor)
    print(f"Sum of linear range sums of distances of the positions from the mean: {fuel_consumption}")



if __name__ == "__main__":
    main()
