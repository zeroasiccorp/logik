#!/usr/bin/env python3

import json
import re
import sys


def main():
    fasm_file = sys.argv[1]
    bitstream_map_file = sys.argv[2]
    json_bitstream_file = sys.argv[3]

    config_bitstream = fasm2bitstream(fasm_file, bitstream_map_file)
    write_bitstream_json(config_bitstream, json_bitstream_file)


def write_bitstream_json(config_bitstream, json_bitstream_file):
    json_out = open(json_bitstream_file, "w")
    json_out.write(json.dumps(config_bitstream))
    json_out.write("\n")
    json_out.close()


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
    # -PG 8/7/2022

    canonical_fasm_feature_list = []

    for feature in fasm_feature_list:
        feature = feature.rstrip()
        if ("=" in feature):
            feature_fields = feature.split("=")
            if (len(feature_fields) != 2):
                print("load_fasm_data() ERROR: wrong number of fields for FASM feature assignment")
            else:
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
                        print("load_fasm_data()",
                              "wrong number of fields for array FASM feature value")
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


def format_binary_bitstream_address(address, address_width):

    formatted_address = format(address, 'b').zfill(address_width)
    return str(address_width) + "'b" + formatted_address
