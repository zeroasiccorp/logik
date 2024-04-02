#!/usr/bin/env python3

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
    chip.input(os.path.join(project_path, 'constraints', f'pin_constraints_{set_part_name}.pcf'))

    # 3. Load target
    chip.load_target(logik_target)

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if __name__ == "__main__":
    main()
