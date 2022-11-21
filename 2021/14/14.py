#!/usr/bin/env python3

import sys
from collections import defaultdict


def occurrences(template, pairs, counts, steps):
    # init counts so that there'll be pairs to start from
    for i in range(len(template) - 1):
        counts[template[i:i+2]] += 1
    
    # for every pair X (e.g. "CB") in the polymer, add the amount of Xs found
    # so far to the amounts of pairs that X decays into ("CH" and "HB").
    # remember to remove pair X count, because all of them transformed into
    # the decayed pairs.
    for _ in range(steps):
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

    # every element will be counted twice due to the way the pairs are added
    # during the insertion steps, except the first and last elements.
    # hence, after incrementing 1st and last element's count, each element's
    # count has to be halved in order to get the real count that would result
    # if the elements were inserted for real.
    individuals = {k: v // 2 for k, v in individuals.items()}

    most_common = max(individuals, key=individuals.get)
    least_common = min(individuals, key=individuals.get)
    diff = individuals[most_common] - individuals[least_common]
    print(f"Most common element: {most_common}")
    print(f"Least common element: {least_common}")
    print(f"{individuals[most_common]} - {individuals[least_common]} = {diff}")
  

def prep_data(lines):
    # since e.g. "CB" turns into "CHB", we know that on the
    # following iteration they will 'decay' into "CH" and "HB".
    # we create a dict and map every pair with their 'decayed' pair of pairs.
    # i.e. {"CB": ["CH", "CB"]}

    template = lines[0]
    pairs = {}
    counts = {}
    for line in lines[1:]:
        pair = line.split(' ')[0]
        insert = line.split(' ')[2]
        pairs[pair] = [pair[0] + insert, insert + pair[1]]
        counts[pair] = 0
    return (template, pairs, counts)


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

    print("Part 1:")
    template, pairs, counts = prep_data(lines)
    occurrences(template, pairs, counts, 10)

    print("\nPart 2:")
    # I don't know why, but counts and pairs need to be re-initialized
    # before running the simulation again
    template, pairs, counts = prep_data(lines)
    occurrences(template, pairs, counts, 40)


if __name__ == "__main__":
    main()