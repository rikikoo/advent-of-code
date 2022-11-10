#!/usr/bin/env python3

import sys
import re

class Vents:
    """
    Stores all vent start and end coordinates.
    Has methods that return a list of coordinates on a hoizontal, vertical or
    diagonal lines.
    Assumes that all coordinates will be on the aforementioned orientations.

    :param coords: a list of all coordinate pairs
    """

    def __init__(self, coords):
        self.vents = coords

    def horizontals(self):
        horiz = []
        for coords in self.vents:
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            if x1 == x2:
                if y1 < y2:
                    ys = list(range(y1, y2 + 1))
                else:
                    ys = list(range(y2, y1 + 1))
                xs = [x1] * len(ys)
                horiz.append(list(zip(xs, ys)))
        return horiz

    def verticals(self):
        verti = []
        for coords in self.vents:
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            if y1 == y2:
                if x1 < x2:
                    xs = list(range(x1, x2 + 1))
                else:
                    xs = list(range(x2, x1 + 1))
                ys = [y1] * len(xs)
                verti.append(list(zip(xs, ys)))
        return verti

    def diagonals(self):
        diago = []
        for coords in self.vents:
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            if x1 != x2 and y1 != y2:
                if x1 < x2:
                    xs = list(range(x1, x2 + 1))
                else:
                    xs = list(reversed(range(x2, x1 + 1)))
                if y1 < y2:
                    ys = list(range(y1, y2 + 1))
                else:
                    ys = list(reversed(range(y2, y1 + 1)))
                diago.append(list(zip(xs, ys)))
        return diago

def count_overlaps(seafloor):
    count = 0
    for row in seafloor:
        for col in row:
            if col > 1:
                count += 1
    return count

def insert_vent(seafloor, vent_line):
    for vent in vent_line:
        seafloor[vent[1]][vent[0]] += 1
    return seafloor

def init_seafloor(dims):
    x = dims[0] + 1
    y = dims[1] + 1
    seafloor = [[0] * x for _ in range(y)]
    return seafloor

def get_coordinates(lines):
    """
    :return: a list of tuples that contain the coordinate pair tuples.
            i.e [
                ((x1a, y1a), (x2a, y2a)),
                ((x1b, y1b), (x2b, y2b)),
                ...
                ]
    """
    xy1 = []
    xy2 = []
    max_x = 0
    max_y = 0
    for line in lines:
        coords = re.findall("[0-9]+", line)
        if len(coords) != 4:
            break
        coords = list(map(int, coords))
        curr_x = max(coords[0], coords[2])
        if curr_x > max_x:
            max_x = curr_x
        curr_y = max(coords[1], coords[3])
        if curr_y > max_y:
            max_y = curr_y
        # append x1, y1 coordinate pair as a tuple
        xy1.append((coords[0], coords[1]))
        # append x2, y2 coordinate pair as a tuple
        xy2.append((coords[2], coords[3]))
    return list(zip(xy1, xy2)), (max_x, max_y)

def main():
    """
    Reads the input text file and converts it into coordinate data.
    Finds overlapping coordinates and produces an answer as per the 'subject04' file.
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

    # get vent coordinates as list of tuples of tuples and the max value of x, y
    coords, dimensions = get_coordinates(lines)
    # create a map of the "sea floor" based on the max values of x and y
    seafloor = init_seafloor(dimensions)
    vents = Vents(coords)

    # place all horizontal/vertical vent lines on seafloor
    horiz = vents.horizontals()
    verti = vents.verticals()
    diago = vents.diagonals()
    for vent in horiz:
        seafloor = insert_vent(seafloor, vent)
    for vent in verti:
        seafloor = insert_vent(seafloor, vent)
    for vent in diago:
        seafloor = insert_vent(seafloor, vent)

    # count the amount of nodes on the sea floor that have more than one vent
    overlaps = count_overlaps(seafloor)
    print(overlaps)

if __name__ == '__main__':
    main()