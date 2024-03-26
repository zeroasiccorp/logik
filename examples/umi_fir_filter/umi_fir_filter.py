#!/usr/bin/env python3

import os

from siliconcompiler import Chip
from ebrick_fpga_cad.targets import ebrick_fpga_target

import lambdalib
import umi


def main(part_name='ebrick_fpga_demo'):
    chip = Chip('umi_fir_filter')

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
    for filename in (
            "tree_adder.v",
            "fir_filter.v",
            "umi_fir_filter.v",
            "umi_fir_filter_output_store.v",
            "umi_fir_filter_regs.v"):
        chip.input(os.path.join(project_path, 'rtl', filename))

    chip.add('option', 'idir', os.path.join(project_path, 'rtl'))

    # import the UMI library
    chip.use(umi)
    chip.add('option', 'library', 'umi')

    # import lambdalib
    chip.use(lambdalib)
    chip.add('option', 'library', 'lambdalib_stdlib')

    # 3. Define constraints
    chip.add('input', 'constraint', 'pinmap',
             os.path.join(project_path, 'constraints', f'pin_constraints_{set_part_name}.json'))

    # 3. Load target
    chip.load_target(ebrick_fpga_target)

    # 4. Customize steps for this design
    chip.add('option', 'define', 'FIR_FILTER_CONSTANT_COEFFS')

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if __name__ == "__main__":
    main()
