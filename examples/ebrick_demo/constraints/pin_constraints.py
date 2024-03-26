import argparse
import json
import math
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

        pin_constraints["clk"] = {
            "direction": 'input',
            "pin": 'clk[0]'
        }

        #***NOTE:  bringing in pin constraints here at the end with update
        #          will allow us to place the boilerplate UMI pin constraints
        #          at the end of the JSON file
        pin_constraints.update(ebrick_fpga_demo.generate_umi_pin_constraints())
    
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
