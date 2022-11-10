#!/usr/bin/env python3

import sys
import re

def sum_of_missed_values(grid, mask):
    summa = 0
    for y, row in enumerate(mask):
        for x, hit in enumerate(row):
            if not hit:
                summa += grid[y][x]
    return summa


def check_for_bingo(mask):
    for row in mask:
        if tuple(row).count(False) == 0:
            return True
    columns = list(zip(*mask))
    for col in columns:
        if col.count(False) == 0:
            return True
    return False

def mark_hit_in_mask(val, grid, mask):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == val:
                mask[y][x] = True
                return mask
    return mask

def play_bingo(draw_list, grids, masks, stop):
    winning_grids = []
    for drawn_value in draw_list:
        for i, grid in enumerate(grids):
            masks[i] = mark_hit_in_mask(drawn_value, grid, masks[i])
            bingo = check_for_bingo(masks[i])
            if bingo:
                winning_grids.append(i)
                res = sum_of_missed_values(grid, masks[i])
                res = res * drawn_value
                if len(set(winning_grids)) == stop:
                    print("Bingo!")
                    return res

def generate_masks(grids):
    """
    Generates a 2D boolean array, where True represents a bingo number match.
    The arrays are initialized to False.

    :param grids: list of grids, a.k.a. lists of rows of integers
    :return: a list of boolean arrays that represent hits on each grid
    """
    masks = []
    for grid in grids:
        size = len(grid[0])
        mask = [[False] * size for n in range(size)]
        masks.append(mask)
    return masks

def get_grids(lines):
    """:return: list of grids, which in turn are lists of rows of integers"""

    grids = []
    grid = []
    for line in lines:
        if line == "\n":
            if len(grid) > 0:
                grids.append(grid)
                grid = []
            continue
        line = re.split(" +", line.strip())
        grid.append(list(map(int, line)))

    return grids

def main():
    """
    Reads the input text file and converts it into bingo grids.
    Then plays bingo and produces an answer as per the 'subject04' file.

    First line of input is a sequence of bingo numbers.
    Rest of the input lines are the bingo grid rows, with each grid separated
    by a line containing only a newline character.
    """

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # just reading each line as strings to a list, no parsing here
            lines = [line for line in f]
    except OSError:
        print(f"Error opening file: {filename}")
        quit()

    # parse input and store formatted data
    draw_list = list(map(int, lines[0].strip().split(',')))
    grids = get_grids(lines[1:])
    # generate a "hit or miss grid" for each bingo number grid
    masks = generate_masks(grids)

    res = play_bingo(draw_list, grids, masks, 1)
    print(f"First bingo result: {res}")
    res = play_bingo(draw_list, grids, masks, len(grids))
    print(f"Last bingo result: {res}")

if __name__ == "__main__":
    main()