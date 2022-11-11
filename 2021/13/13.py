#!/usr/bin/env python3

import sys


def fold_grid(grid, x, y):
    pass

def fill_grid(coords, grid):
    for x, y in coords:
        grid[y][x] = '#'
    return grid

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

    x = []
    y = []
    folds = []
    for line in lines:
        if 'fold' not in line:
            tmp = line.split(',')
            x.append(int(tmp[0]))
            y.append(int(tmp[1]))
        elif 'fold' in line:
            fold = line.split(' ')[2].split('=')
            folds.append((fold[0], int(fold[1])))

    max_x = max(x)
    max_y = max(y)
    coords = list(zip(x, y))
    grid = [['.'] * (max_x + 1) for i in range(max_y + 1)]
    grid = fill_grid(coords, grid)

    for row in grid:
        for col in row:
            print(col, end=' ')
        print('')

    folded = fold_grid(grid, folds)

if __name__ == "__main__":
    main()