#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import json
import math
import numpy as np
import re
import sys


def main():
    fasm_file = sys.argv[1]
    bitstream_map_file = sys.argv[2]
    json_bitstream_file = sys.argv[3]
    dat_bitstream_file = sys.argv[4]
    bin_bitstream_file = sys.argv[5]

    config_bitstream = fasm2bitstream(fasm_file, bitstream_map_file)
    write_bitstream_json(config_bitstream, json_bitstream_file)
    flattened_bitstream = generate_flattened_bitstream(config_bitstream)
    write_bitstream_data(flattened_bitstream, dat_bitstream_file)
    binary_bitstream = format_binary_bitstream(flattened_bitstream)
    write_bitstream_binary(binary_bitstream, bin_bitstream_file)


def write_bitstream_json(config_bitstream, json_bitstream_file):
    json_out = open(json_bitstream_file, "w")
    json_out.write(json.dumps(config_bitstream))
    json_out.write("\n")
    json_out.close()


def write_bitstream_data(config_bitstream, dat_bitstream_file):
    dat_out = open(dat_bitstream_file, "w")
    for entry in config_bitstream:
        dat_out.write(f'{entry}\n')
    dat_out.close()


def write_bitstream_binary(binary_bitstream, binary_bitstream_file):
    binary_bitstream.tofile(binary_bitstream_file)


def calculate_bitstream_columns(bitstream_map):

    return len(bitstream_map)


def calculate_bitstream_rows(bitstream_map):

    max_rows = -1
    # ***TO DO:  Add SC-compliant error checking that
    #            the row count is constant across columns
    #            (or eventually allow non-constant count
    #            for non-rectangular FPGAs)
    for i in range(len(bitstream_map)):
        if (len(bitstream_map[i]) > max_rows):
            max_rows = len(bitstream_map[i])

    return max_rows


def calculate_address_size(bitstream_map):

    max_length = 0

    for x in range(len(bitstream_map)):
        for y in range(len(bitstream_map[x])):
            if (len(bitstream_map[x][y]) > max_length):
                max_length = len(bitstream_map[x][y])

    return max_length


def calculate_config_data_width(bitstream_map):

    # ***TO DO:  The config data width is supposed to be
    #            constant for all addresses, so we should
    #            add error checking to see if it ever
    #            deviates.  Need an SC-compliant way to do
    #            this before implementing
    max_config_width = 0
    for x in range(len(bitstream_map)):
        for y in range(len(bitstream_map[x])):
            for address in range(len(bitstream_map[x][y])):
                if (len(bitstream_map[x][y][address]) > max_config_width):
                    # To prevent runaway runtimes, assume that the config
                    # width is constant throughout the bitstream map
                    # and abort after we find a positive value
                    max_config_width = len(bitstream_map[x][y][address])
                    break

    return max_config_width


# In this converter, the bitstream address space is flattened
# into a vector; this is useful for prepping the bitstream for
# storage into a ROM that will be loaded over a serial interface
# To align to the bitstream ordering that is required by
# the bitstream loading circuit, it is necessary to do some
# arithmetic to pick which configuration words go in which
# order in the flattened vector; see below for details
def generate_flattened_bitstream(bitstream_map):

    # Convert FPGA array dimensions into address space bit widths;
    # this will assist in flattening the address space:
    num_bitstream_columns = calculate_bitstream_columns(bitstream_map)
    num_bitstream_rows = calculate_bitstream_rows(bitstream_map)
    address_length = int.bit_length(calculate_address_size(bitstream_map))
    x_length = int.bit_length(num_bitstream_columns - 1)
    y_length = int.bit_length(num_bitstream_rows - 1)

    # Get the word size of the words in the bitstream
    config_data_width = calculate_config_data_width(bitstream_map)

    input_bus_width = x_length + y_length + address_length

    default_entry = format(0, "0x").zfill(int(config_data_width / 4))

    bitstream_vector = [default_entry] * pow(2, input_bus_width)

    for x in range(len(bitstream_map)):
        for y in range(len(bitstream_map[x])):
            for address in range(len(bitstream_map[x][y])):

                vector_address = y * pow(2, x_length + address_length)
                vector_address += x * pow(2, address_length)
                vector_address += address

                bitstream_data = concatenate_data(bitstream_map[x][y][address])
                formatted_data = format(bitstream_data, "0x").zfill(int(config_data_width / 4))
                bitstream_vector[vector_address] = formatted_data

    return bitstream_vector


def concatenate_data(data_array):

    data_sum = 0
    scale_factor = 1

    for i in range(len(data_array)):
        if (data_array[i] == 1):
            data_sum += scale_factor
        scale_factor = scale_factor * 2

    return data_sum


def get_bitstream_map_location(base_address,
                               umi_addr_offset,
                               umi_column_index,
                               config_words_per_address,
                               umi_addresses_per_row,
                               num_bitstream_columns,
                               num_bitstream_rows,
                               max_bitstream_address,
                               bitstream_size,
                               reverse=False):

    base_position = base_address / config_words_per_address / umi_addresses_per_row
    y = math.floor(base_position / max_bitstream_address)
    x = config_words_per_address * umi_addr_offset + umi_column_index
    addr = int(base_position) % max_bitstream_address

    if (reverse):
        y = num_bitstream_rows - y - 1
        addr = max_bitstream_address - addr - 1

    return x, y, addr


def format_binary_bitstream(bitstream_data, word_size=8):

    converted_data = []

    for element in bitstream_data:
        element_temp = int(element.rstrip(), 16)
        sub_element_count = math.ceil(word_size / 8)
        for i in range(sub_element_count):
            cur_data_word = element_temp & ((1 << 8) - 1)
            converted_data.append(cur_data_word)
            element_temp = element_temp >> 8

    bitstream_data_array = np.array(converted_data, np.uint8)

    return bitstream_data_array


def fasm2bitstream(fasm_file, bitstream_map_file, verbose=False, fasm_warnings=False):

    with open(bitstream_map_file, "r") as map_file:
        json_bitstream_map = json.load(map_file)
        bitstream_map = json_bitstream_map["bitstream"]

    fasm_features = load_fasm_data(fasm_file, all_warnings=fasm_warnings, verbose=verbose)

    config_bitstream = generate_bitstream_from_fasm(bitstream_map, fasm_features)

    return config_bitstream


def load_fasm_data(filename, all_warnings=False, verbose=False):
    fasm_file = open(filename, "r")
    fasm_feature_list = fasm_file.readlines()

    # "Canonicalize" the feature list, as described here:
    # https://fasm.readthedocs.io/en/latest/specification/syntax.html

    canonical_fasm_feature_list = []

    for feature in fasm_feature_list:
        feature = feature.rstrip()
        if ("=" in feature):
            feature_fields = feature.split("=")
            if (len(feature_fields) == 2):
                feature_name = feature_fields[0]
                feature_value = feature_fields[1]

                # ***TO DO:  Select a more robust detector of a multibit feature
                #            than array index colon checking
                if (":" in feature_name):

                    errors = 0

                    feature_split_pattern = r'[\[\]:]'
                    feature_name_fields = re.split(feature_split_pattern, feature_name)

                    # ***ASSUMPTION: All FASM feature output will be binary
                    feature_array = feature_value.split("'b")

                    if (len(feature_name_fields) < 2):
                        errors += 1

                    else:
                        base_feature_length = int(feature_array[0])
                        base_feature_value = feature_array[1]

                        if (base_feature_length != len(base_feature_value)):
                            errors += 1

                    if (len(feature_name_fields) < 3):
                        errors += 1

                    if (errors == 0):
                        base_feature_name = feature_name_fields[0]
                        base_feature_name_msb = int(feature_name_fields[1])

                        for i in range(len(base_feature_value)):
                            # multi-bit fasm features are represented big-endian, so:
                            if (base_feature_value[i] == "1"):
                                cur_index = base_feature_name_msb - i
                                indexed_feature_name = f"{base_feature_name}[{cur_index}]"
                                canonical_fasm_feature_list.append(indexed_feature_name)

                else:
                    if (feature_value != 0):
                        canonical_fasm_feature_list.append(feature_name)

        else:
            canonical_fasm_feature_list.append(feature)

    return canonical_fasm_feature_list


def generate_bitstream_from_fasm(address_map,
                                 fasm_data,
                                 verbose=False):

    feature_index = invert_address_map(address_map)
    bitstream = []
    for x in range(len(address_map)):
        bitstream.append([])
        for y in range(len(address_map[x])):
            bitstream[x].append([])
            for address in range(len(address_map[x][y])):
                bitstream[x][y].append([0] * len(address_map[x][y][address]))

    for fasm_feature in fasm_data:
        x_i = feature_index[fasm_feature]['x']
        y_i = feature_index[fasm_feature]['y']
        addr_i = feature_index[fasm_feature]['address']
        bit_i = feature_index[fasm_feature]['bit']
        bitstream[x_i][y_i][addr_i][bit_i] = 1

    return bitstream


def invert_address_map(address_map):

    feature_index = {}
    for x in range(len(address_map)):
        for y in range(len(address_map[x])):
            for address in range(len(address_map[x][y])):
                for bit in range(len(address_map[x][y][address])):
                    feature_index[address_map[x][y][address][bit]] = {}
                    feature_index[address_map[x][y][address][bit]]['x'] = x
                    feature_index[address_map[x][y][address][bit]]['y'] = y
                    feature_index[address_map[x][y][address][bit]]['address'] = address
                    feature_index[address_map[x][y][address][bit]]['bit'] = bit

    return feature_index


if __name__ == "__main__":
    main()
