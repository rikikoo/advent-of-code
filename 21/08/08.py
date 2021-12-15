#!/usr/bin/env python3

import sys


class Display:
    """
    Takes segments as a list of strings and parses them and figures out which is which.
    Read the provided 'subject08' for more info.

    :param segments: list of strings, which represent segments of single digits, in order from 0 to 9
    """

    def __init__(self, segments):
        self.a = ''     # top
        self.b = ''     # top-left
        self.c = ''     # top-right
        self.d = ''     # middle
        self.e = ''     # bottom-left
        self.f = ''     # bottom-right
        self.g = ''     # bottom
        self.one = ""
        self.seven = ""
        self.four = ""
        self.eight = ""
        self.twothreefive = []
        self.zerosixnine = []
        self.parse_segments(segments)
        self.solve_segments()

    def parse_segments(self, segments):
        for segment in segments:
            len_seg = len(segment)
            if len_seg == 2:
                self.one = segment
            elif len_seg == 3:
                self.seven = segment
            elif len_seg == 4:
                self.four = segment
            elif len_seg == 5:
                self.twothreefive.append(segment)
            elif len_seg == 6:
                self.zerosixnine.append(segment)
            else:
                self.eight = segment

    def solve_segments(self):
        # 'a' segment derived from comparing 1 and 7, 'c' and 'f' as leftovers
        cf = ''
        for seg in self.seven:
            if seg not in self.one:
                self.a = seg
            else:
                cf += seg

        # segments 'b' and 'd' are the ones not already found in 4
        bd = ''
        for seg in self.four:
            if seg not in cf:
                bd += seg
        found_segments = set(self.a + cf + bd)

        # 9 has only one segment that isn't known yet: 'g'
        for seg_set in self.zerosixnine:
            diff = set(seg_set).difference(found_segments)
            if len(diff) == 1:
                self.g = list(diff)[0]
        found_segments.add(self.g)

        # 2 is the only digit that has a distinct unidentified segment
        for seg_set in self.twothreefive:
            diff = set(seg_set).difference(found_segments)
            if len(diff) == 1:
                self.e = list(diff)[0]

        # using the identified segments and 1's segments, extrapolate 'b' from 0...
        found_segments = set(self.a + self.e + self.g + cf)
        for seg_set in self.zerosixnine:
            diff = set(seg_set).difference(found_segments)
            if len(diff) == 1:
                self.b = list(diff)[0]
        # ...and 'd' from 3
        for seg_set in self.twothreefive:
            diff = set(seg_set).difference(found_segments)
            if len(diff) == 1:
                self.d = list(diff)[0]

        # ...and 'f' from 6, now using only the identified segments...
        found_segments = set(self.a + self.b + self.d + self.e + self.g)
        for seg_set in self.zerosixnine:
            diff = set(seg_set).difference(found_segments)
            if len(diff) == 1:
                self.f = list(diff)[0]
        # ...and finally the leftover segment has to be 'c'
        found_segments.add(self.f)
        self.c = list(set(cf).difference(found_segments))[0]

    def print_segments(self):
        print(f" {self.a * 4} ")
        print(f"{self.b}    {self.c}")
        print(f"{self.b}    {self.c}")
        print(f" {self.d * 4} ")
        print(f"{self.e}    {self.f}")
        print(f"{self.e}    {self.f}")
        print(f" {self.g * 4} ")

    def count_unique_digits(self, digits):
        count = 0
        uniques = [set(self.one), set(self.seven), set(self.four), set(self.eight)]
        for digit in digits:
            if set(digit) in uniques:
                count += 1
        return count

    def get_digit(self, digit):
        d_set = set(digit)
        if len(d_set) == 2:
            return 1
        elif len(d_set) == 3:
            return 7
        elif len(d_set) == 4:
            return 4
        elif len(d_set) == 7:
            return 8
        elif len(d_set) == 5:
            if self.b not in d_set and self.f not in d_set:
                return 2
            elif self.b not in d_set and self.e not in d_set:
                return 3
            else:
                return 5
        elif len(d_set) == 6:
            if self.d not in d_set:
                return 0
            elif self.c not in d_set:
                return 6
            else:
                return 9
        else:
            return -1


def parse_input(lines):
    segments = []
    digits = []
    for line in lines:
        split_line = line.strip().split('|')
        segments.append(split_line[0].strip().split(' '))
        digits.append(split_line[1].strip().split(' '))
    return segments, digits


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # reading input lines to a list of strings
            lines = [line for line in f if line != "\n"]
    except OSError:
        print(f"Error opening file: {filename}")
        quit()

    segments, digit_sets = parse_input(lines)
    displays = []
    for segment in segments:
        displays.append(Display(segment))

    unique_count = 0
    output_values = []
    for i, digits in enumerate(digit_sets):
        unique_count += displays[i].count_unique_digits(digits)
        power = 3
        val = 0
        for digit in digits:
            val += displays[i].get_digit(digit) * (10 ** power)
            power -= 1
        output_values.append(val)
    print(f"Unique segment digits in output values: {unique_count}")

    print("Output values:")
    total = 0
    for val in output_values:
        print(val)
        total += val
    print(f"Sum of output values: {total}")
    #displays[0].print_segments()


if __name__ == "__main__":
    main()
