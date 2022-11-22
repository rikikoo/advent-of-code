#!/usr/bin/env python3

import sys
import queue


def is_inbounds(pos, dims):
    return pos[0] >= 0 and pos[0] <= dims[0] and pos[1] > 0 and pos[1] <= dims[1]

def heuristic(end, adjacent):
    return abs(end[0] - adjacent[0]) + abs(end[1] - adjacent[1])

def neighbours(x, y):
    # return non-diagonal neighbours in clockwise order (12, 3, 6, 9 o'clock)
    return [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

def a_star(grid, source, target):
    cost_so_far = {}
    prev = {}
    q = queue.PriorityQueue()

    cost_so_far[source] = 0
    prev[source] = None
    q.put(source, 0)

    while not q.empty():
        curr = q.get()
        if curr == target:
            break
        for adj in neighbours(curr[0], curr[1]):
            if not is_inbounds(adj, target):
                continue
            new_cost = cost_so_far[curr] + grid[adj[1]][adj[0]]
            if adj not in prev or new_cost < cost_so_far[adj]:
                cost_so_far[adj] = new_cost
                priority = new_cost + heuristic(target, adj)
                q.put(adj, priority)
                prev[adj] = curr
    return prev

def retrace_path(grid, trace, target):
    path = []
    risk = 0
    curr = (target)
    while curr != (0, 0):
        path.append(curr)
        risk += grid[curr[1]][curr[0]]
        curr = trace[curr]
    path.append(curr)
    return risk, path

def highlight_path(grid, path):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if (x, y) in path:
                print(f"\x1b[35m{int(col)}\x1b[0m", end='')
            else:
                print(col, end='')
        print('')

def expand_grid(grid, dims):
    grids = []
    grids.append(grid)
    g = 0
    for i in range(24):
        if i != 0 and i % 4 == 0:
            g = i - 4
        new_grid = []
        for row in grids[g]:
            new_row = []
            for col in row:
                new_val = 1 if col == 9 else col + 1
                new_row.append(new_val)
            new_grid.append(new_row)
        grids.append(new_grid)
        g += 1

    final_grid = []
    start = 0
    end = 5
    while end <= 25:
        for y in range(dims[1] + 1):
            row = []
            for i, grid in enumerate(grids[start:end]):
                row += grid[y]
            final_grid.append(row)
        if i != 0 and i % 4 == 0:
            start += 5
            end += 5
    
    return final_grid

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

    # part 1
    grid = [[int(val) for val in line] for line in lines]
    x = len(grid[0]) - 1
    y = len(grid) - 1    
    trace = a_star(grid, (0, 0), (x, y))
    risk, path = retrace_path(grid, trace, (x, y))
    highlight_path(grid, path)
    print(f"\nRisk of the path above: {risk}\n\n")

    # part 2
    grid = expand_grid(grid, (x, y))
    x = len(grid[0]) - 1
    y = len(grid) - 1
    trace = a_star(grid, (0, 0), (x, y))
    risk, path = retrace_path(grid, trace, (x, y))
    highlight_path(grid, path)
    print(f"\nRisk of the path above: {risk}\n")

if __name__ == "__main__":
    main()
