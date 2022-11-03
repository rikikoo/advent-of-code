#!/usr/bin/env python3

import sys


def dfs(g, source, curr_node, visits, max_visits, paths):
    print(f"{source} -> {curr_node}")
    if curr_node == "end":
        paths += 1
        return paths
    adjacent = g[curr_node]
    for a in adjacent:
        if visits[a] < max_visits:
            if a.islower() and a != "end":
                visits[a] += 1
            paths = dfs(g, curr_node, a, visits.copy(), max_visits, paths)
    return paths


def get_paths(g, max_visits):
    visits = {}
    [visits.setdefault(key, 0) for key in g.keys()]
    visits["start"] = 2
    paths = 0
    paths = dfs(g, "none", "start", visits, max_visits, paths)
    return paths


def get_graph(lines):
    """
    Couldn't bother with venv issues on VS Code,
    so I wrote my own mini 'networkx'
    """

    # store all edges in a list
    connections = []
    start = False
    end = False
    for connection in lines:
        conn = tuple(connection.strip().split('-'))
        if len(conn) != 2:
            print(f"ERROR: incorrect connection format: {connection}")
            quit()
        if "start" in conn:
            start = True
        if "end" in conn:
            end = True
        connections.append(conn)
    if not start or not end:
        print("ERROR: 'start' and/or 'end' missing from connections")
        quit()
    
    # construct graph dictionary
    g = {}
    for (n1, n2) in connections:
        if n1 not in g.keys():
            g[n1] = set([n2])
        else:
            g[n1].add(n2)
        if n2 not in g.keys():
            g[n2] = set([n1])
        else:
            g[n2].add(n1)
    
    return g        


def main():
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # read input to a list of strings
            lines = [line for line in f if line != "\n"]
    except OSError:
        print(f"ERROR: could not open file {filename}")
        quit()

    g = get_graph(lines)

    paths = get_paths(g, 1)
    print(f"Part 1 answer: {paths}")

    # paths = get_paths(g, 2)
    # print(f"Part 2 answer: {paths}")



if __name__ == "__main__":
    main()
