#!/usr/bin/env python3

import os

import siliconcompiler
from ebrick_fpga_cad.targets import ebrick_fpga_target


def main(part_name='ebrick_fpga_demo'):
    
    top_module = 'dp_memory_8192x32'
    
    chip = siliconcompiler.Chip(f'{top_module}')

    if (__name__ == '__main__') :
        chip.create_cmdline(switchlist=['-fpga_partname'])

    # Set default part name
    chip.set('fpga', 'partname', part_name, clobber=False)
        
    set_part_name = chip.get('fpga', 'partname')
    
    # 1. Defining the project

    # 2. Define source files
    project_path = os.path.abspath(__file__).replace('dp_memory_8192x32.py','')
    src_files = [
        "dp_memory_generic.v",
        "dp_memory_8192x32.v",
    ]
    
    for filename in src_files :
        chip.input(os.path.join(project_path, 'rtl', filename))

    # 3. Define constraints
    chip.add('input', 'constraint', 'pinmap',
             os.path.join(project_path, 'constraints', f'pin_constraints_{set_part_name}.json'))
    
    # 4. Load target
    chip.load_target(ebrick_fpga_target)

    # 5. Customize steps for this design
    chip.set('option', 'quiet', True)
    
    chip.run()
    chip.summary()

if __name__ == "__main__":
    main()
