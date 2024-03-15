#!/usr/bin/env python3

import argparse
import os

import siliconcompiler
from ebrick_fpga_cad.targets import ebrick_fpga_target

from fir_filter_pin_constraints import generate_mapped_constraints
from fir_filter_pin_constraints import write_json_constraints


def main(part_name='ebrick_fpga_demo'):
    
    top_module = 'fir_filter_wrapper'
    
    chip = siliconcompiler.Chip(f'{top_module}')

    if (__name__ == '__main__') :
        chip.create_cmdline(switchlist=['-fpga_partname'])
    else :
        chip.set('fpga', 'partname', part_name)
        
    set_part_name = chip.get('fpga', 'partname')
    
    # 1. Defining the project

    # 2. Define source files
    project_path = os.path.abspath(__file__).replace('sc/fir_filter.py','')
    src_files = [
        "tree_adder.v",
        "fir_filter.v",
        "fir_filter_wrapper.v",
    ]
    
    # 3. Define constraints
    # chip.add('input', 'constraint', 'pins', 'fir_filter_pin_constraints.xml')
    pinmap_file = os.path.join(project_path, 'sc', f'fir_filter_pin_constraints_{set_part_name}.json')

    pin_constraints = generate_mapped_constraints(set_part_name)
    write_json_constraints(pin_constraints, pinmap_file)
    
    chip.add('input', 'constraint', 'pinmap', pinmap_file)
    
    for filename in src_files :
        chip.input(os.path.join(project_path, 'rtl', filename))

    # 3. Load target
    chip.load_target(ebrick_fpga_target)

    # 4. Customize steps for this design
    chip.add('option', 'define', 'FIR_FILTER_CONSTANT_COEFFS')
    
    chip.run()


if __name__ == "__main__":
    main()
