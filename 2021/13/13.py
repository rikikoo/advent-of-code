#!/usr/bin/env python3

import sys

class Grid():
    def __init__(self, lines) -> None:
        self.max_x = 0
        self.max_y = 0
        self.folds = []
        self.coords = self.parse_data(lines)
        self.grid = self.make_grid()

    def parse_data(self, lines) -> list:
        x = []
        y = []
        for line in lines:
            if 'fold' not in line:
                tmp = line.split(',')
                x.append(int(tmp[0]))
                y.append(int(tmp[1]))
            elif 'fold' in line:
                fold = line.split(' ')[2].split('=')
                self.folds.append((fold[0], int(fold[1])))
        
        self.max_x = max(x)
        self.max_y = max(y)
        return list(zip(x, y))

    def make_grid(self) -> list:
        grid = [[False] * (self.max_x + 1) for i in range(self.max_y + 1)]
        for x, y in self.coords:
            grid[y][x] = True
        return grid

    def count(self):
        return sum([sum(row) for row in self.grid])

    def show(self):
        for row in self.grid:
            for col in row:
                if col:
                    print(f"\x1b[35m{int(col)}\x1b[0m", end=' ')
                else:
                    print(int(col), end=' ')
            print('')
    
    def show_halves(top, bottom):
        for row in bottom:
            for col in row:
                if col:
                    print(f"\x1b[38m{int(col)}\x1b[0m", end=' ')
                else:
                    print(int(col), end=' ')
            print('')
        print('')
        for row in top:
            for col in row:
                if col:
                    print(f"\x1b[38m{int(col)}\x1b[0m", end=' ')
                else:
                    print(int(col), end=' ')
            print('')
        print('')


    def do_fold(self, fold, halves=False):
        folded_grid = []
        if fold[0] == 'x':
            bottom = []
            top = []
            for row in self.grid:
                bottom.append(row[:fold[1]])
                top.append(row[:fold[1]:-1])
            if len(top) >= len(bottom):
                self.max_x = len(top) - 1
            else:
                self.max_x = len(bottom) - 1
            for i, row in enumerate(bottom):
                tmp = [False] * (len(top) - len(bottom))
                top[i] = ([False] * (len(bottom) - len(top))) + top[i]
                bottom[i] = bottom[i] + tmp
        else:
            top = self.grid[:fold[1]:-1]
            bottom = self.grid[:(fold[1])]
            if len(top) >= len(bottom):
                self.max_y = len(top) - 1
            else:
                self.max_y = len(bottom) - 1
            tmp = bottom + ([False] * (len(top) - len(bottom)))
            top = ([False] * (len(bottom) - len(top))) + top
            bottom = tmp

        if halves:
            self.show_halves(top, bottom)

        folded_grid = []
        for i, row in enumerate(bottom):
            if i == self.max_y + 1:
                break
            if len(row) == 1:
                folded_grid.append(top[i] or bottom[i])
            else:
                folded_grid.append([t or b for t, b in zip(top[i], bottom[i])])
        self.grid = folded_grid



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

    grid = Grid(lines)
    for i, fold in enumerate(grid.folds):
        print(f"fold {i+1:3}: {fold}")
        grid.do_fold(fold)
        if i == 0:
            print(f"Part 1 answer: {grid.count()}\n")

    print("\nPart 2 answer (eight capital letters):\n")
    grid.show()


if __name__ == "__main__":
    main()