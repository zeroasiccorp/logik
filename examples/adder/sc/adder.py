
import argparse
import os

import siliconcompiler
from ebrick_fpga_cad.targets import ebrick_fpga_target

from adder_pin_constraints import generate_mapped_constraints
from adder_pin_constraints import write_json_constraints

def main():

    top_module = 'adder'
    
    chip = siliconcompiler.Chip(f'{top_module}')

    additional_args = {
        '-part_name': {
            'type': str,
        }
    }
    
    args = chip.create_cmdline('sc',
                               additional_args=additional_args)

    part_name = args['part_name']
    
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

    pin_constraints = generate_mapped_constraints(part_name)
    write_json_constraints(pin_constraints, pinmap_file)
    
    chip.add('input', 'constraint', 'pinmap', pinmap_file)
    
    for filename in src_files :
        chip.input(os.path.join(project_path, 'rtl', filename))

    # 3. Load target
    chip.load_target(ebrick_fpga_target)

    chip.run()


if __name__ == "__main__":
    main()
