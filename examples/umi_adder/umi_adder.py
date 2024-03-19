#!/usr/bin/env python3

import os

from siliconcompiler import Chip
from ebrick_fpga_cad.targets import ebrick_fpga_target

import umi
import lambdalib

def main(part_name='ebrick_fpga_demo'):
    chip = Chip('umi_adder')

    if __name__ == '__main__':
        chip.create_cmdline(
            switchlist=[
                '-fpga_partname'
            ])

    # import the UMI library
    chip.use(umi)
    chip.add('option', 'library', 'umi')

    # import lambdalib
    chip.use(lambdalib)
    chip.add('option', 'library', 'lambdalib_stdlib')

    # Set default part name
    chip.set('fpga', 'partname', part_name, clobber=False)

    set_part_name = chip.get('fpga', 'partname')

    # 1. Defining the project

    # 2. Define source files
    project_path = os.path.abspath(os.path.dirname(__file__))
    chip.input(os.path.join(project_path, 'rtl', 'umi_adder.v'))

    # 3. Define constraints
    chip.add('input', 'constraint', 'pinmap',
             os.path.join(project_path, 'constraints', f'pin_constraints_{set_part_name}.json'))
    
    # 3. Load target
    chip.load_target(ebrick_fpga_target)

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if __name__ == "__main__":
    main()
