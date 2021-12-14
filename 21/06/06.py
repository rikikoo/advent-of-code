#!/usr/bin/env python3

import sys


def simulate_n_days(days_to_birth, fish_count, n):
    while n:
        next_day = [0] * 9
        for day, fish in enumerate(days_to_birth):
            if day == 0:
                fish_count += fish      # new fish are born
                next_day[-1] = fish     # allocate new fish to 9th day
                next_day[-3] += fish    # allocate old fish to 7th day
            elif day == 7:
                next_day[day - 1] += fish   # don't overwrite old fish reset day
            else:
                next_day[day - 1] = fish    # move every fish a day closer to birth
        n -= 1
        days_to_birth = next_day
    return fish_count


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # assuming that input is a single line of comma separated integers
            fish = tuple(map(int, f.readline().strip().split(',')))
    except OSError:
        print(f"Error opening file: {filename}")
        quit()

    # create a list where the value at each index of the list represents
    # the number of fish on that number of days before giving birth
    days_to_birth = []
    for n in range(9):
        days_to_birth.append(fish.count(n))

    # execute 80-day simulation
    res = simulate_n_days(days_to_birth, len(fish), 80)
    print(f"fish after 80 days: {res}")
    res = simulate_n_days(days_to_birth, len(fish), 256)
    print(f"fish after 256 days: {res}")


if __name__ == "__main__":
    main()
