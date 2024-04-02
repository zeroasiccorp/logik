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


def main(part_name='logik_demo'):
    chip = Chip('adder')

    if __name__ == '__main__':
        chip.create_cmdline(
            switchlist=[
                '-fpga_partname'
            ])

    # Set default part name
    chip.set('fpga', 'partname', part_name, clobber=False)

    set_part_name = chip.get('fpga', 'partname')

    # 1. Defining the project

    # 2. Define source files
    project_path = os.path.abspath(os.path.dirname(__file__))
    chip.input(os.path.join(project_path, 'rtl', 'adder.v'))

    # 3. Define constraints
    chip.add('input', 'constraint', 'pinmap',
             os.path.join(project_path, 'constraints', f'pin_constraints_{set_part_name}.json'))

    # 3. Load target
    chip.load_target(logik_target)

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if __name__ == "__main__":
    main()
