#!/usr/bin/env python3

import sys
import numpy as np
from time import sleep


CLEAR = "\033[2J"
GREY = "\033[90m"
WHITE = "\033[97m"
RESET = "\033[0m"


def get_adjacent_values(grid):
    # this method is from SO (CC BY-SA 3.0):
    # https://stackoverflow.com/a/38078596/14656436
    region = 10  # number of region whose neighbors we want

    y = grid == region  # convert to Boolean

    rolled = np.roll(y, 1, axis=0)  # shift down
    rolled[0, :] = False
    z = np.logical_or(y, rolled)

    rolled = np.roll(y, -1, axis=0)  # shift up
    rolled[-1, :] = False
    z = np.logical_or(z, rolled)

    rolled = np.roll(y, 1, axis=1)  # shift right
    rolled[:, 0] = False
    z = np.logical_or(z, rolled)

    rolled = np.roll(y, -1, axis=1)  # shift left
    rolled[:, -1] = False
    z = np.logical_or(z, rolled)

    neighbors = set(np.unique(np.extract(z, grid))) - {region}
    print(neighbors)


def get_adjacent_positions(pos, limits):
    a_list = []
    x = pos[1]
    y = pos[0]
    # row above current position
    if y > 0:
        if x > 0:
            a_list.append((y - 1, x - 1))
        a_list.append((y - 1, x))
        if x < limits[1]:
            a_list.append((y - 1, x + 1))
    # cell right of current position
    if x < limits[1]:
        a_list.append((y, x + 1))
    # row below current position
    if y < limits[0]:
        if x < limits[1]:
            a_list.append((y + 1, x + 1))
        a_list.append((y + 1, x))
        if x > 0:
            a_list.append((y + 1, x - 1))
    # cell left of current position
    if x > 0:
        a_list.append((y, x - 1))

    return a_list


def update_adjacent(grid, pos, limits, orig_pos):
    x = pos[1]
    y = pos[0]
    o_x = orig_pos[1]
    o_y = orig_pos[0]
    adj_list = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1),     # row above
                (y, x - 1), (y, x + 1),                         # current row
                (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]     # row below
    for adj in adj_list:
        if -1 in adj or limits[0] in adj or limits[1] in adj or grid[adj] > 9:
            continue
        grid[adj] += 1
        # update adjacent cells recursively if a new flashing cell
        # is "behind" original (recursion origin) position
        if grid[adj] > 9 and (adj[0] < o_y or (adj[1] < o_x and adj[0] == o_y)):
            grid = update_adjacent(grid, adj, limits, orig_pos)
    return grid


def print_grid(grid):
    print(CLEAR)
    flash = False
    for row in grid:
        for val in row:
            if val == 0:
                print(f"{WHITE}{str(val)}{RESET}", end='')
                flash = True
            else:
                print(f"{GREY}{str(val)}{RESET}", end='')
        print('')
    if flash:
        sleep(0.5)
    else:
        sleep(0.25)


def simulate_flashes(grid):
    limits = (len(grid), len(grid[0]))
    grid_size = limits[0] * limits[1]
    flash_count = 0
    flash100 = 0
    n = 1
    while n:
        grid = grid + 1
        for y in range(limits[0]):
            for x in range(limits[1]):
                if grid[y, x] > 9:
                    grid = update_adjacent(grid, (y, x), limits, (y, x))
        grid = np.where(grid > 9, 0, grid)
        flashes = np.count_nonzero(grid == 0)
        flash_count += flashes
        print_grid(grid)
        if flashes == grid_size:
            break
        if n == 100:
            flash100 = flash_count
            print(f"Flashes after 100 steps: {flash100}")
            print("Continue in 10 sec...")
            sleep(10)
        n += 1
    return n, flash100


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # convert input to numpy.ndarray
            grid = np.array([[val for val in line.strip()] for line in f if line != '\n'], dtype="int")
    except OSError:
        print(f"Error opening file: {filename}")
        quit()

    steps, flash100 = simulate_flashes(grid)
    print(f"Flashes after 100 steps: {flash100}")
    print(f"Whole grid flashed on step: {steps}")


if __name__ == "__main__":
    main()
