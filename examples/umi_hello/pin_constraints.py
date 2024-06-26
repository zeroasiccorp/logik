#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import argparse
import json
import os

from logik.templates.logik_demo.umi_pin_constraints \
    import generate_umi_pin_constraints


def main():
    option_parser = argparse.ArgumentParser()
    # Command-line options
    option_parser.add_argument(
        "part_name",
        nargs='?',
        default="logik_demo",
        help="specify part number to prep, or specify all to build all parts in parts catalog"
    )

    options = option_parser.parse_args()
    part_name = options.part_name

    pin_constraints = generate_mapped_constraints(part_name)

    write_json_constraints(
        pin_constraints,
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     f"pin_constraints_{part_name}.pcf"))


def generate_mapped_constraints(part_name):

    pin_constraints = {}

    if (part_name == 'logik_demo'):
        pin_constraints["clk"] = {
            "direction": 'input',
            "pin": 'clk[0]'
        }

        pin_constraints["nreset"] = {
            "direction": 'input',
            "pin": 'gpio_in[0]'
        }

        pin_constraints.update(
            generate_umi_pin_constraints(
                umi_ports_used=[1],
                port_types=[
                    "uhost_req",
                    "udev_req"
                ],
                index_control_bits=False
            )
        )
    else:
        print(f"ERROR: unsupported part name {part_name}")

    return pin_constraints


def write_json_constraints(constraints, filename):
    with (open(filename, 'w')) as json_file:
        json_file.write(json.dumps(constraints, indent=2))
        json_file.write('\n')
        json_file.close()


if __name__ == "__main__":
    main()
