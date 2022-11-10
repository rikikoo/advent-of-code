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


def find_lowest_positions(floor, overlay, limits):
    x_lim = limits[1]
    y_lim = limits[0]
    # iterate over seafloor
    y = 0
    while y <= y_lim:
        x = 0
        while x <= x_lim:
            # update overlay
            overlay[y, x] = check_surroundings(floor, (y, x), (y_lim, x_lim))
            x += 1
        y += 1
    return overlay


def flood_fill(floor, overlay, start, limits, depth):
    surr = get_surrounding_pos(start, limits)
    for adjacent in surr:
        if floor[adjacent] != 9 and overlay[adjacent] == 0:
            depth += 1
            overlay[adjacent] = 1
            overlay, depth = flood_fill(floor, overlay, adjacent, limits, depth)
    return overlay, depth


def get_lowest(floor, overlay):
    low_points = []
    low_positions = []
    for y, row in enumerate(overlay):
        for x, lowest in enumerate(row):
            if lowest:
                low_points.append(floor[y][x])
                low_positions.append((y, x))
    return low_points, low_positions


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

    # init overlay matrix that will store min value positions
    overlay = np.zeros(floor.shape, dtype="int")
    # get edge row and column of matrix
    limits = (len(floor) - 1, len(floor[0]) - 1)

    # find values and positions of single lowest points
    overlay = find_lowest_positions(floor, overlay, limits)
    low_points, low_positions = get_lowest(floor, overlay)
    print(f"Sum of risk levels of lowest points: {sum(low_points) + len(low_points)}")

    # do flood fill starting from each lowest point position
    basins = []
    for pos in low_positions:
        overlay, basin_size = flood_fill(floor, overlay, pos, limits, 1)
        basins.append(basin_size)
    # find three largest basins
    result = np.sort(basins)[-3:]
    print(result.prod())


if __name__ == "__main__":
    main()
