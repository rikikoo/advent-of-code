#!/usr/bin/env python3

import sys


def parse_paths(p):
    paths = []
    path = []
    for i, node in enumerate(p):
        if node[1] == "end":
            prev = p[i - 1::-1]
            last = p[i][0]
            path.append(node[1])
            for elem in prev:
                if elem[0] == last - 1 and elem[1] != "end":
                    path.append(elem[1])
                    last = elem[0]
            paths.append(list(reversed(path)))
            path = []
        elif i < len(p) - 1:
            if p[i][0] == p[i + 1][0] and p[i + 1] == "end":
                del p[i]
    return paths


def dfs(g, visited, start, path, n):
    path.append((n, start))
    print(f"{n}: {start}")
    if start == "end":
        return path
    adjacent = g[start]
    has_upper = True in [x.isupper() for x in adjacent]
    for adj in adjacent:
        if not visited[adj]:
            if str(adj).islower() and adj != "end":
                visited[adj] = True
            path = dfs(g, visited, adj, path, n + 1)
        if start == "start":
            visited.update((k, False) for (k, v) in visited.items())
            visited["start"] = True
    return path


def get_paths(g):
    visited = {}
    [visited.setdefault(key, False) for key in g.keys()]
    visited["start"] = True
    path = dfs(g, visited, "start", [], 1)
    return path


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
    path = get_paths(g)
    paths = parse_paths(path)
    for path in paths:
        print(path)

    part1ans = 0
    for path in paths:
        count = 0
        for node in path:
            if node not in ["start", "end"] and node.islower():
                count += 1
        if count <= 1:
            part1ans += 1
    print(f"Paths that visit a small cave at most once: {part1ans}")


if __name__ == "__main__":
    main()
