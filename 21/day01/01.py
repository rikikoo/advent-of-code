#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <input filename>")
    quit()

filename = sys.argv[1]
try:
    with open(filename) as f:
        values = [int(line) for line in f if line != "\n"]
except OSError:
    print(f"Error opening filename: {filename}")
    quit()

count = 0
for i, val in enumerate(values):
    if i == 0:
        continue
    if val > values[i - 1]:
        count += 1

print(count)