#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <input filename>")
    quit()

filename = sys.argv[1]
try:
    with open(filename) as f:
        # assuming that every line isthe same length and clean i.e. "<numerical_value>\n"
        bitmap = [[int(bit) for bit in line if bit != "\n"] for line in f if line != "\n"]
except OSError:
    print(f"Error opening file: {filename}")
    quit()

# zip bit-rows and use tuple.count() to find most common bit
res_list = []
bits = zip(*bitmap)
for column in bits:
    res_list.append(column.count(1) > column.count(0))
# convert resulting boolean list to list of 0s and 1s
bit_list = list(map(int, res_list))

# create a bitmask, also a list of bits (all 1s in this case)
mask_str = '1' * len(bitmap[0])
mask_list = [int(n) for n in mask_str]

# the following list-of-bits-to-integer method shamelessly stolen from SO
# https://stackoverflow.com/a/12461400/14656436
gamma = 0
for bit in bit_list:
    gamma = (gamma << 1) | bit
mask = 0
for bit in mask_list:
    mask = (mask << 1) | bit
epsilon = gamma ^ mask

print(f"gamma rate: {gamma}")
print(f"epsilon rate: {epsilon}")
print(f"power consumption: {gamma * epsilon}")