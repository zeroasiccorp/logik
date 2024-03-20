#!/usr/bin/env python3

import json
import math
import numpy as np
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


def write_bitstream_data(config_bitstream, dat_bitstream_file):
    dat_out = open(dat_bitstream_file, "w")
    for entry in config_bitstream:
        dat_out.write(f'{entry}\n')
    dat_out.close()

    
def write_bitstream_binary(binary_bitstream, binary_bitstream_file):
    binary_bitstream.tofile(binary_bitstream_file)


def calculate_bitstream_columns(bitstream_map):
    
    return len(bitstream_map)


def calculate_bitstream_rows(bitstream_map) :

    max_rows = -1
    #***TO DO:  Add SC-compliant error checking that
    #           the row count is constant across columns
    #           (or eventually allow non-constant count
    #           for non-rectangular FPGAs)
    for i in range(len(bitstream_map)) :
        if (len(bitstream_map[i]) > max_rows) :
            max_rows = len(bitstream_map[i])

    return max_rows
    

def calculate_address_length(bitstream_map) :

    return get_max_bitstream_address_length(bitstream_map)


def calculate_config_data_width(bitstream_map):

    #***TO DO:  The config data width is supposed to be
    #           constant for all addresses, so we should
    #           add error checking to see if it ever
    #           deviates.  Need an SC-compliant way to do
    #           this before implementing
    max_config_width = 0
    for x in range(len(bitstream_map)):
        for y in range(len(bitstream_map[x])):
            for address in range(len(bitstream_map[x][y])):
                if (len(bitstream_map[x][y][address]) > max_config_width) :
                    #To prevent runaway runtimes, assume that the config
                    #width is constant throughout the bitstream map
                    #and abort after we find a positive value
                    max_config_width = len(bitstream_map[x][y][address])
                    break

    return max_config_width


#The native bitstream in this flow organizes data into a 4-D array
#The first dimension is the X-coordinate in the VPR model
#The second dimension is the Y coordinate in the VPR model
#The third coordinate is an address within the X,Y coordinate
#that maps to a <config_data_width> wide word in the bitstream
#The fourth coordinate is the bit index in the word at
#(X, Y, address)
#The job of this function is to reformat that map into a vector
#of words that are the full width of whatever UMI port is being
#used to do bitstream loading on the FPGA.  It does this by
#measuring the dimensions of the bitstream that it receives and
#using those dimensions to map the bitstream data to a vector
#of words that are the same width as the UMI data bus.
#Currently it is assumed that the bitstream loader on the FPGA
#receives data over UMI in such a way that data for a particular
#array (X,Y) coordinate must be assigned to a fixed position
#within the UMI data bus (i.e. if (0, 1) data comes in on
#umi_data[7:0] once, it must do so always).  To enforce this
#alignment, zero-padding the UMI data may be necessary depending on
#the FPGA array size, and this function takes care of that too.
#In this implementation, the array that is returned passes back one
#bitstream word per array element, so it's up to the receiver
#of this data to assemble it into UMI words of the correct size
def generate_umi_bitstream(bitstream_map,
                           umi_rom_data_width=256,
                           reverse=True,
                           show_map=False,
                           verbose=False):

    num_bitstream_columns = calculate_bitstream_columns(bitstream_map)
    num_bitstream_rows = calculate_bitstream_rows(bitstream_map)
    address_length = calculate_address_length(bitstream_map)
    config_data_width = calculate_config_data_width(bitstream_map)
    x_length = int.bit_length(num_bitstream_columns-1)
    y_length = int.bit_length(num_bitstream_rows-1)
        
    if ((config_data_width != 8) and
        (config_data_width != 16) and
        (config_data_width != 32)) :
        exit()
            
    umi_bitstream = []

    if (umi_rom_data_width > config_data_width) :
        bitstream_addresses_per_rom_address = int(math.ceil(umi_rom_data_width / config_data_width))
    else :
        bitstream_addresses_per_rom_address = 1

    config_words_per_address= int(umi_rom_data_width / config_data_width)
    
    umi_addresses_per_row = int(math.ceil(num_bitstream_columns / bitstream_addresses_per_rom_address))

    num_column_slots = umi_addresses_per_row * bitstream_addresses_per_rom_address
    num_padding_slots = num_column_slots - num_bitstream_columns

    bitstream_address_width = x_length + y_length + address_length

    bitstream_size = calculate_bitstream_size(bitstream_map, num_column_slots)

    max_tile_bitstream_size = get_max_bitstream_address_length(bitstream_map)
    
    if (reverse) :
        start_address = bitstream_size - bitstream_addresses_per_rom_address
        stop_address = -1
        address_increment = -1 * bitstream_addresses_per_rom_address * umi_addresses_per_row
    else :
        start_address = 0;
        stop_address = bitstream_size
        address_increment = bitstream_addresses_per_rom_address * umi_addresses_per_row

    for address in range(start_address, stop_address, address_increment) :
            
        for k in range(umi_addresses_per_row) :
            for j in range(config_words_per_address-1, -1, -1) :

                x, y, addr = get_bitstream_map_location(address,
                                                        k,
                                                        j,
                                                        config_words_per_address,
                                                        umi_addresses_per_row,
                                                        num_bitstream_columns,
                                                        num_bitstream_rows,
                                                        max_tile_bitstream_size,
                                                        bitstream_size,
                                                        reverse=False)

                if (x >= num_bitstream_columns) :
                    umi_bitstream.append(format(0, "0x").zfill(int(config_data_width/4)))

                else :

                    address_in_range = check_bitstream_map_address(x, y, addr, bitstream_map)

                    if (address_in_range) :
                        bitstream_data = concatenate_data(bitstream_map[x][y][addr])
                    else :
                        bitstream_data = 0

                    formatted_bitstream_data = format(bitstream_data, "0x").zfill(int(config_data_width/4))
                    umi_bitstream.append(formatted_bitstream_data)

    return umi_bitstream

def concatenate_data(data_array) :

    data_sum = 0
    scale_factor = 1
    
    for i in range(len(data_array)) :
        if (data_array[i] == 1) :
            data_sum += scale_factor
        scale_factor = scale_factor * 2

    return data_sum


def check_bitstream_map_address(x, y, addr, bitstream_map) :

    in_range = True
    if ((x < len(bitstream_map)) == False) :
        in_range = False
    elif ((y < len(bitstream_map[x])) == False) :
        in_range = False
    elif ((addr < len(bitstream_map[x][y])) == False) :
        in_range = False
    else :
        in_range = True

    return in_range

def get_bitstream_map_location(base_address,
                               umi_addr_offset,
                               umi_column_index,
                               config_words_per_address,
                               umi_addresses_per_row,
                               num_bitstream_columns,
                               num_bitstream_rows,
                               max_bitstream_address,
                               bitstream_size,
                               reverse=False) :

    y = math.floor(base_address / max_bitstream_address / config_words_per_address / umi_addresses_per_row)
    x = config_words_per_address * umi_addr_offset + umi_column_index
    addr = int(base_address / config_words_per_address / umi_addresses_per_row) % max_bitstream_address

    if (reverse) :
        y = num_bitstream_rows - y - 1
        addr = max_bitstream_address - addr - 1
    
    return x, y, addr


def calculate_bitstream_size(bitstream_map, num_column_slots) :

    bitstream_size = len(bitstream_map) * num_column_slots * get_max_bitstream_address_length(bitstream_map)
    return bitstream_size

def get_max_bitstream_address_length(bitstream_map) :

    max_length = 0
    
    for x in range(len(bitstream_map)) :
        for y in range(len(bitstream_map[x])) :
            if (len(bitstream_map[x][y]) > max_length) :
                max_length = len(bitstream_map[x][y])

    return max_length


def format_binary_bitstream(bitstream_data):

    converted_data = []

    for element in bitstream_data:
        element_temp = int(element.rstrip(), 16)
        data_lsb = element_temp & ((1 << 64) - 1)
        data_msb = (element_temp >> 64) & ((1 << 64) - 1)
        
        converted_data.append(data_lsb)
        converted_data.append(data_msb)
        
    bitstream_data_array = np.array(converted_data, np.uint64)
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
