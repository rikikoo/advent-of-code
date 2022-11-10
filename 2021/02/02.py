#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <input filename>")
    quit()

filename = sys.argv[1]
try:
    with open(filename) as f:
        # assuming that every line is clean i.e. "<direction> <numerical_value>\n"
        movements = [line.split(' ') for line in f if line != "\n"]
except OSError:
    print(f"Error opening file: {filename}")
    quit()

horiz = 0
verti = 0
aim = 0
for move in movements:
    if move[0] == "forward":
        horiz += int(move[1])
        if aim:
            verti += (int(move[1]) * aim)
    elif move[0] == "down":
        aim += int(move[1])
    else:
        aim -= int(move[1])

print(f"final\n\t...horizontal pos: {horiz}\n\t...vertical pos: {verti}\n\t...aim: {aim}")
print(f"\nproduct of positions: {horiz * verti}")