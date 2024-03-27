#!/usr/bin/env python3

import os

from ebrick_demo import ebrick

from siliconcompiler import Chip
from ebrick_fpga_cad.targets import ebrick_fpga_target


def main(part_name='ebrick_fpga_demo'):
    chip = Chip('ebrick_demo_fpga')

    if __name__ == '__main__':
        chip.create_cmdline(switchlist=['-fpga_partname'])

    # Set default part name
    chip.set('fpga', 'partname', part_name, clobber=False)

    set_part_name = chip.get('fpga', 'partname')

    # 1. Project setup
    ebrick.setup_core_design(chip)

    # Add this repository as a package source to pick up a top level wrapper
    chip.register_package_source(
        name='ebrick_fpga_demo',
        path=os.path.abspath(os.path.dirname(__file__)))

    # Add the wrapper around ebrick_core to map it to a valid ebrick_fpga_demo pinout
    chip.input(os.path.join('rtl', 'ebrick_core_fpga_wrapper.v'), package='ebrick_fpga_demo')

    # Set the top module to ebrick_core
    chip.set('option', 'entrypoint', 'ebrick_core_fpga_wrapper')

    # 3. Define constraints
    chip.add('input', 'constraint', 'pinmap',
             os.path.join('constraints', f'pin_constraints_{set_part_name}.json'),
             package='ebrick_fpga_demo')

    # 3. Load target
    chip.load_target(ebrick_fpga_target)

    # 4. Customize steps for this design

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if __name__ == "__main__":
    main()
