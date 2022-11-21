#!/usr/bin/env python3

import sys
from collections import defaultdict

def occurrences(template, pairs, counts, n):
    # init counts so there're pairs to start from
    for i in range(len(template) - 1):
        counts[template[i:i+2]] += 1
    
    for _ in range(n):
        tmp = counts.copy()
        for k, v in counts.items():
            if v > 0:
                tmp[pairs[k][0]] += v
                tmp[pairs[k][1]] += v
                tmp[k] -= v
        counts = tmp

    individuals = defaultdict(int)
    for k, v in counts.items():
        individuals[k[0]] += v
        individuals[k[1]] += v
        if k[0] == k[1]:
            individuals[k[1]] += 1
    individuals[template[0]] += 1
    individuals[template[-1]] += 1

    most_common = max(individuals, key=individuals.get)
    least_common = min(individuals, key=individuals.get)
    diff = individuals[most_common] // 2 - individuals[least_common] // 2
    print(f"Most common element: {most_common}")
    print(f"Least common element: {least_common}")
    print(f"{individuals[most_common] // 2} - {individuals[least_common] // 2} = {diff}")
    if n == 40:
        print(f"...and if we're doing 40 steps then half the result (again, for some reason): {diff // 2}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()
    filename = sys.argv[1]
    try:
        with open(filename) as f:
            lines = [line.strip() for line in f if line != '\n']
    except OSError:
        print(f"Error opening file: {filename}")
        quit()

    template = lines[0]
    pairs = {}
    counts = {}
    for line in lines[1:]:
        pair = line.split(' ')[0]
        insert = line.split(' ')[2]
        pairs[pair] = [pair[0] + insert, insert + pair[1]]
        counts[pair] = 0

    print("Part 1:")
    occurrences(template, pairs, counts, 10)
    print("\nPart 2:")
    occurrences(template, pairs, counts, 40)


if __name__ == "__main__":
    main()