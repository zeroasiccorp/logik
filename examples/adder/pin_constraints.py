# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import argparse
import json
import os


def main():
    option_parser = argparse.ArgumentParser()
    # Command-line options
    option_parser.add_argument(
        "part_name",
        help="specify part number to prep, or specify all to build all parts in parts catalog")

    options = option_parser.parse_args()
    part_name = options.part_name

    if (part_name == "raw"):
        pin_constraints = generate_raw_constraints()
    else:
        pin_constraints = generate_mapped_constraints(part_name)

    write_json_constraints(
        pin_constraints,
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     f"pin_constraints_{part_name}.pcf"))


def generate_mapped_constraints(part_name):

    pin_constraints = {}

    if (part_name == 'logik_demo'):

        for i in range(8):
            pin_constraints[f'a[{i}]'] = {
                "direction": "input",
                "pin": f'gpio_in[{i}]'
            }

        for i in range(8):
            pin_constraints[f'b[{i}]'] = {
                "direction": "input",
                "pin": f'gpio_in[{i + 8}]'
            }

        for i in range(9):
            pin_constraints[f'y[{i}]'] = {
                "direction": "output",
                "pin": f'gpio_out[{i + 16}]'
            }

    else:
        print(f"ERROR: unsupported part name {part_name}")

    return pin_constraints


def generate_raw_constraints():

    pin_constraints = {}

    for i in range(8):
        pin_constraints[f'a[{i}]'] = {
            "direction": "input",
            "pin": f'pad_in_1_2[{i}]'
        }

    for i in range(8):
        pin_constraints[f'b[{i}]'] = {
            "direction": "input",
            "pin": f'pad_in_1_3[{i}]'
        }

    for i in range(9):
        if (i < 8):
            pin_constraints[f'y[{i}]'] = {
                "direction": "output",
                "pin": f'pad_out_1_4[{i}]'
            }
        else:
            pin_constraints[f'y[{i}]'] = {
                "direction": "output",
                "pin": f'pad_out_1_5[{i - 8}]'
            }

    return pin_constraints


def write_json_constraints(constraints, filename):

    with (open(filename, 'w')) as json_file:
        json_file.write(json.dumps(constraints, indent=2))
        json_file.write('\n')
        json_file.close()


if __name__ == "__main__":
    main()
