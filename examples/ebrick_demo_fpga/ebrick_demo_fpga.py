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

from ebrick_demo import ebrick

from siliconcompiler import Chip
from logik.targets import logik_target


def main(part_name='logik_demo'):
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
        name='logik_demo',
        path=os.path.abspath(os.path.dirname(__file__)))

    # Add the wrapper around ebrick_core to map it to a valid logik_demo pinout
    chip.input(os.path.join('rtl', 'ebrick_core_fpga_wrapper.v'), package='logik_demo')

    # Set the top module to ebrick_core
    chip.set('option', 'entrypoint', 'ebrick_core_fpga_wrapper')

    # 3. Define constraints
    chip.add('input', 'constraint', 'pinmap',
             os.path.join('constraints', f'pin_constraints_{set_part_name}.json'),
             package='logik_demo')

    # 3. Load target
    chip.load_target(logik_target)

    # 4. Customize steps for this design

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if __name__ == "__main__":
    main()
