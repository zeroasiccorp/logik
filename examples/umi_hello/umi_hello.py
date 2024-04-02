#!/usr/bin/env python3

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

import os

from siliconcompiler import Chip
from logik.targets import logik_target


def setup(chip, part_name=None):
    # 1. Defining the project
    # Set default part name
    if not part_name:
        part_name = 'logik_demo_mini'
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
        chip.add('input', 'constraint', 'pinmap',
                 os.path.join('constraints', f'pin_constraints_{part_name}.json'),
                 package='umi_hello')


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
