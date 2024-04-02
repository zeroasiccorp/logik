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
import json
import os

import ebrick_fpga_cad.templates.ebrick_fpga_demo.umi_pin_constraints as ebrick_fpga_demo


def main():
    option_parser = argparse.ArgumentParser()
    # Command-line options
    option_parser.add_argument(
        "part_name",
        help="specify part number to prep, or specify all to build all parts in parts catalog")

    options = option_parser.parse_args()
    part_name = options.part_name

    pin_constraints = generate_mapped_constraints(part_name)

    write_json_constraints(
        pin_constraints,
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     f"pin_constraints_{part_name}.json"))


def generate_mapped_constraints(part_name):

    pin_constraints = {}

    if (part_name == 'ebrick_fpga_demo'):

        pin_constraints["fpga_clk[0]"] = {
            "direction": 'input',
            "pin": 'clk[0]'
        }

        pin_constraints["fpga_clk[1]"] = {
            "direction": 'input',
            "pin": 'clk[1]'
        }

        pin_constraints["fpga_clk[2]"] = {
            "direction": 'input',
            "pin": 'clk[2]'
        }

        pin_constraints["nreset"] = {
            "direction": 'input',
            "pin": 'gpio_in[0]'
        }

        pin_constraints["go"] = {
            "direction": 'input',
            "pin": 'gpio_in[1]'
        }

        pin_constraints["testmode"] = {
            "direction": 'input',
            "pin": 'gpio_in[2]'
        }

        pin_constraints["jtag_tck"] = {
            "direction": 'input',
            "pin": 'gpio_in[3]'
        }

        pin_constraints["jtag_tms"] = {
            "direction": 'input',
            "pin": 'gpio_in[4]'
        }

        pin_constraints["jtag_tdi"] = {
            "direction": 'input',
            "pin": 'gpio_in[5]'
        }

        pin_constraints["jtag_tdo"] = {
            "direction": 'output',
            "pin": 'gpio_out[6]'
        }

        pin_constraints["jtag_tdo_oe"] = {
            "direction": 'output',
            "pin": 'gpio_out[7]'
        }

        for i in range(16):
            pin_constraints[f"no_rxgpio[{i}]"] = {
                "direction": 'input',
                "pin": f'gpio_in[{i + 16}]'
            }
        for i in range(16):
            pin_constraints[f"no_txgpio[{i}]"] = {
                "direction": 'output',
                "pin": f'gpio_out[{i + 32}]'
            }
        for i in range(16):
            pin_constraints[f"no_txgpio_oe[{i}]"] = {
                "direction": 'input',
                "pin": f'gpio_out[{i + 48}]'
            }

        # ***NOTE:  bringing in pin constraints here at the end with update
        #           will allow us to place the boilerplate UMI pin constraints
        #           at the end of the JSON file
        umi_pins = ebrick_fpga_demo.generate_umi_pin_constraints(umi_data_width=32,
                                                                 umi_ports_used=[1, 2, 3],
                                                                 port_types=["uhost_req",
                                                                             "uhost_resp",
                                                                             "udev_req",
                                                                             "udev_resp"],
                                                                 umi_port_num_offset=1,
                                                                 index_control_bits=True)
        pin_constraints.update(umi_pins)

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
