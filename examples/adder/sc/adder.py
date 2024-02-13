
import argparse
import os

import siliconcompiler
from ebrick_fpga_cad.targets import ebrick_fpga_target


def main(part_name='zafg1um_0202'):

    top_module = 'adder'
    
    chip = siliconcompiler.Chip(f'{top_module}')

    chip.set('fpga', 'partname', part_name)

    # 1. Defining the project

    # 2. Define source files
    project_path = os.path.abspath(__file__).replace('sc/adder.py','')
    src_files = [
        'adder.v',
    ]

    # 3. Define constraints
    # chip.add('input', 'constraint', 'pins', 'adder_pin_constraints.xml')
    pinmap_file = os.path.join(project_path, 'sc', f'adder_pin_constraints_{part_name}.json')
    chip.add('input', 'constraint', 'pinmap', pinmap_file)
    
    for filename in src_files :
        chip.input(os.path.join(project_path, 'rtl', filename))

    # 3. Load target
    chip.load_target(ebrick_fpga_target)

    chip.run()


if __name__ == "__main__":
    option_parser = argparse.ArgumentParser("ebrick-fpga CAD adder Demo")
    option_parser.add_argument("-part_name", default="zafg1um_0202")
    options = option_parser.parse_args()
    main(part_name=options.part_name)
