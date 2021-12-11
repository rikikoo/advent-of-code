#!/usr/bin/env python3

import sys

def bits_to_int(bit_list):
    # the following list-of-bits-to-integer method stolen from SO
    # https://stackoverflow.com/a/12461400/14656436
    res = 0
    for bit in bit_list:
        res = (res << 1) | bit
    return res

def get_criterion(bitmap, column, mode):
    if column >= len(bitmap[0]):
        return
    # zip bit-rows and use tuple.count() to find most common bit
    bits = zip(*bitmap)
    bit_column = list(bits)[column]
    if mode == 0:   # O2 generator (most common)
        res = (bit_column.count(1) >= bit_column.count(0))
    else:           # CO2 scrubber (least common)
        res = not (bit_column.count(1) >= bit_column.count(0))
    return int(res)

def parse_bits(bitmap, mode):
    bit_list = bitmap.copy()
    i_bit = 0
    while len(bit_list) > 1:
        inclusion_criterion = get_criterion(bit_list, i_bit, mode)
        tmp_list = []
        for bits in bit_list:
            if bits[i_bit] == inclusion_criterion:
                tmp_list.append(bits)
        bit_list = tmp_list
        i_bit += 1
    return bit_list


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input filename>")
        quit()

    filename = sys.argv[1]
    try:
        with open(filename) as f:
            # assuming that every line is the same length and clean i.e. "<numerical_value>\n"
            bitmap = [[int(bit) for bit in line if bit != "\n"] for line in f if line != "\n"]
    except OSError:
        print(f"Couldn't open file: {filename}\nPlease check that the file exists.")
        quit()

    # get O2 generator value
    o2_list = parse_bits(bitmap, 0)
    o2 = bits_to_int(o2_list[0])
    # get CO2 scrubber value
    co2_list = parse_bits(bitmap, 1)
    co2 = bits_to_int(co2_list[0])

    # get gamma value
    gamma_list = []
    for i, bit in enumerate(bitmap[0]):
        gamma_list.append(get_criterion(bitmap, i, 1))
    gamma = bits_to_int(gamma_list)

    # create a bitmask, also a list of bits (all 1s in this case)
    mask_str = '1' * len(bitmap[0])
    mask_list = [int(n) for n in mask_str]
    mask = bits_to_int(mask_list)
    # XOR gamma with mask to flip the bits
    epsilon = gamma ^ mask

    print(f"gamma rate: {gamma}")
    print(f"epsilon rate: {epsilon}")
    print(f"power consumption: {gamma * epsilon}\n")
    print(f"O2 generator: {o2}")
    print(f"CO2 scrubber: {co2}")
    print(f"life support rating: {o2 * co2}")

if __name__ == "__main__":
    main()