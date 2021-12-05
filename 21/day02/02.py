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
    print(f"Error opening filename: {filename}")
    quit()

horiz = 0
verti = 0
for move in movements:
    if move[0] == "forward":
        horiz += int(move[1])
    elif move[0] == "down":
        verti += int(move[1])
    else:
        verti -= int(move[1])

print(f"horizontal pos: {horiz}\nvertical pos: {verti}")
print(f"product of positions: {horiz * verti}")