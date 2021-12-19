#!/usr/bin/env python3

import sys


def label_line(line):
    # use a first-in-last-out stack to match brackets
    filo = []
    for c in line:
        if c == '(':
            filo.insert(0, c)
        elif c == '[':
            filo.insert(0, c)
        elif c == '{':
            filo.insert(0, c)
        elif c == '<':
            filo.insert(0, c)
        elif c == ')' and filo.pop(0) != '(':
            return -1, [c]
        elif c == ']' and filo.pop(0) != '[':
            return -1, [c]
        elif c == '}' and filo.pop(0) != '{':
            return -1, [c]
        elif c == '>' and filo.pop(0) != '<':
            return -1, [c]

    # line is valid or incomplete if no illegal closing brackets found.
    # valid if filo is empty, otherwise incomplete.
    return 1, filo


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # reading input lines to a list
            lines = [line.strip() for line in f if line != '\n']
    except OSError:
        print(f"Error opening file: {filename}")
        quit()

    # parse and label lines
    labels = {
        "error_char": [],
        "illegal": [],
        "incomplete": [],
        "stack": []
    }
    for line in lines:
        ret, filo = label_line(line)
        if ret < 0:
            labels["error_char"].append(filo[0])
            labels["illegal"].append(line)
        else:
            labels["incomplete"].append(line)
            labels["stack"].append(filo)

    # count syntax error score for illegal lines
    score = 0
    for invalid in labels["error_char"]:
        if invalid == ')':
            score += 3
        elif invalid == ']':
            score += 57
        elif invalid == '}':
            score += 1197
        elif invalid == '>':
            score += 25137
    print(f"Illegal line error score: {score}")

    # count syntax error score for incomplete lines
    score_list = []
    for filo in labels["stack"]:
        score = 0
        for expected in filo:
            score *= 5
            if expected == '(':
                score += 1
            elif expected == '[':
                score += 2
            elif expected == '{':
                score += 3
            elif expected == '<':
                score += 4
        score_list.append(score)

    txt = "Median of incomplete line error scores: {}"
    print(txt.format(sorted(score_list)[len(score_list) // 2]))


if __name__ == "__main__":
    main()
