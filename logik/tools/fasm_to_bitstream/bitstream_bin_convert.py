#!/usr/bin/env python3

###############################################################################
# Copyright 2024 Zero ASIC Corporation
#
# Licensed under the MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY,WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ----
#
##############################################################################

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
