# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import siliconcompiler

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
        chip.error('FPGA partname has not been set.', fatal=True)

    # 2.  Load all available FPGAs
    chip.use(logik_demo)

    if part_name not in chip.getkeys('fpga'):
        chip.error(f'{part_name} has not been loaded', fatal=True)

    # 3. Load flow
    chip.use(logik_flow)

    # 4. Select default flow
    chip.set('option', 'mode', 'fpga', clobber=False)
    chip.set('option', 'flow', 'logik_flow', clobber=False)


#########################
if __name__ == "__main__":
    target = siliconcompiler.Chip('<target>')
    setup(target)
    target.write_manifest('target.json')
