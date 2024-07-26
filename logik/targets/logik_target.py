# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler import Chip, SiliconCompilerError

from logik.fpgas import logik_demo
from logik.flows import logik_flow


####################################################
# Target Setup
####################################################
def setup(chip):
    '''
    Demonstration target for running the open-source fpgaflow.
    '''

    # 1. Configure fpga part
    part_name = chip.get('fpga', 'partname')
    if not part_name:
        raise ValueError('FPGA partname has not been set.')

    # 2.  Load all available FPGAs
    chip.use(logik_demo)

    if part_name not in chip.getkeys('fpga'):
        raise SiliconCompilerError(f'{part_name} has not been loaded')

    # 3. Load flow
    chip.use(logik_flow)

    # 4. Select default flow
    chip.set('option', 'flow', 'logik_flow', clobber=False)


#########################
if __name__ == "__main__":
    target = Chip('<target>')
    setup(target)
    target.write_manifest('target.json')
