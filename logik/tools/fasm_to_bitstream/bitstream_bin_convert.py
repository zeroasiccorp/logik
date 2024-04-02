#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import argparse


def main():

    option_parser = argparse.ArgumentParser()

    option_parser.add_argument("binary_bitstream",
                               help="binary bitstream file")
    option_parser.add_argument("ascii_bitstream",
                               help="ascii bitstream file")

    options = option_parser.parse_args()

    bin_filename = options.binary_bitstream
    out_filename = options.ascii_bitstream

    words = []
    with open(bin_filename, 'rb') as bin_file:
        for cur_byte in bin_file.read():
            formatted_word = format(cur_byte, "0x").zfill(2)
            words.append(formatted_word)

    with open(out_filename, 'w') as out_file:
        for word in words:
            out_file.write(word)
            out_file.write('\n')


if __name__ == "__main__":
    main()
