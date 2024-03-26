import argparse
import json
import math
import os


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


def generate_mapped_constraints(part_name, data_width=16, num_taps=8):

    output_width = int(2 * data_width + math.log2(num_taps))

    pin_constraints = {}

    if (part_name == 'ebrick_fpga_demo'):

        pin_constraints["clk"] = {
            "direction": 'input',
            "pin": 'clk[0]'
        }
        pin_constraints["resetn"] = {
            "direction": 'input',
            "pin": 'gpio_in[1]'
        }
        pin_constraints["input_valid"] = {
            "direction": 'input',
            "pin": 'gpio_in[2]'
        }
        pin_constraints["output_valid"] = {
            "direction": 'output',
            "pin": 'gpio_out[3]'
        }

        for i in range(data_width):
            pin_constraints[f'x[{i}]'] = {
                "direction": "input",
                "pin": f'gpio_in[{i+4}]'
            }

        for i in range(output_width):
            pin_constraints[f'y[{i}]'] = {
                "direction": "output",
                "pin": f'gpio_out[{i+data_width+4}]'
            }

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
