#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import os

from siliconcompiler import Chip
from logik.targets import logik_target


def setup(chip, part_name=None):
    # 1. Defining the project
    # Set default part name
    if not part_name:
        part_name = 'logik_demo'
    chip.set('fpga', 'partname', part_name, clobber=False)
    part_name = chip.get('fpga', 'partname')

    # Add this repo as a package source
    chip.register_package_source(
        name='umi_hello',
        path=os.path.abspath(os.path.dirname(__file__)))

    # 2. Define source files
    chip.input(os.path.join('rtl', 'umi_hello.v'), package='umi_hello')

    # 3. Load target
    chip.load_target(logik_target)

    # 4. Define constraints
    if chip.get('option', 'mode') == 'fpga':
        chip.input(os.path.join('constraints', f'pin_constraints_{part_name}.pcf'),
                   package="umi_hello")


def main(part_name=None):
    chip = Chip('umi_hello')

    if __name__ == '__main__':
        chip.create_cmdline(
            switchlist=[
                '-fpga_partname'
            ])

    # Setup chip object with design files
    setup(chip, part_name=part_name)

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if __name__ == "__main__":
    main()
