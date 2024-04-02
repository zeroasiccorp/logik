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

import siliconcompiler
from siliconcompiler.targets import utils

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

    # 4. Setup default show tools
    utils.set_common_showtools(chip)

    # 5. Select default flow
    chip.set('option', 'mode', 'fpga', clobber=False)
    chip.set('option', 'flow', 'logik_flow', clobber=False)


#########################
if __name__ == "__main__":
    target = siliconcompiler.Chip('<target>')
    setup(target)
    target.write_manifest('target.json')
