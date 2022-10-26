#!/usr/bin/env python3

import sys


class Path:
    """
    Since there's no real way to pass objects by reference in Python,
    classes are necessary.

    Keeps track of paths found by the depth-first search algorithm.
    Stores only paths that lead to the 'end' node.
    """

    def __init__(self):
        self.path = ["start"]
        self.paths = []

    def apnd(self, node):
        self.path.append(node)
        if node == "end":
            self.paths.append(self.path)


def dfs(g, curr_node, visited, paths, curr_path):
    if curr_node == "end":
        paths.append(curr_path)
        return paths
    adjacent = g[curr_node]
    curr_visits = visited
    for a in adjacent:
        if visited[a] == False:
            if a.islower():
                curr_visits[a] = True
            curr_path.append(a)
            paths = dfs(g, a, curr_visits, paths, curr_path)
    return paths


def get_paths(g):
    visited = {}
    [visited.setdefault(key, False) for key in g.keys()]
    visited["start"] = True
    paths = Path()
    paths = dfs(g, paths)
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
    paths = get_paths(g)


    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
