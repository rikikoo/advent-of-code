#!/usr/bin/env python3

import sys
import numpy as np


def get_surrounding_pos(pos, limits):
    valids = []
    if pos[1] != 0:
        valids.append((pos[0], pos[1] - 1))
    if pos[1] < limits[1]:
        valids.append((pos[0], pos[1] + 1))
    if pos[0] != 0:
        valids.append((pos[0] - 1, pos[1]))
    if pos[0] < limits[0]:
        valids.append((pos[0] + 1, pos[1]))
    return valids


def check_surroundings(floor, curr_pos, limits):
    surr = get_surrounding_pos(curr_pos, limits)
    heights = []
    for adjacent in surr:
        heights.append(floor[adjacent])
    if min(heights) > floor[curr_pos]:
        return 1
    else:
        return 0


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # reading input lines and storing them as a 2D np.array
            floor = np.array([[int(n) for n in line if n.isdigit()] for line in f if line != '\n'])
    except OSError:
        print(f"Error opening file: {filename}")
        quit()

    # init overlay matrix that will store min values
    overlay = np.zeros(floor.shape, dtype="int")
    # get edge row and column of matrix
    x_lim = len(floor[0]) - 1
    y_lim = len(floor) - 1
    # iterate over seafloor
    y = 0
    while y <= y_lim:
        x = 0
        while x <= x_lim:
            # update overlay
            overlay[y, x] = check_surroundings(floor, (y, x), (y_lim, x_lim))
            x += 1
        y += 1

    # find all low points on the seafloor map
    low_points = []
    for y, row in enumerate(overlay):
        for x, lowest in enumerate(row):
            if lowest:
                low_points.append(floor[y][x])

    # for line in floor:
    #     for n in line:
    #         print(str(n), end='')
    #     print('')
    # print('')
    # for line in overlay:
    #     for n in line:
    #         print(str(n), end='')
    #     print('')
    print(f"Sum of risk levels: {sum(low_points) + len(low_points)}")


if __name__ == "__main__":
    main()
