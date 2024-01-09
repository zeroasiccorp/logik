#zafg1um.py

import siliconcompiler
from siliconcompiler.targets import utils


from ebrick_fpga_cad.fpgas import zafg1um
from ebrick_fpga_cad.flows import ebrick_fpga_flow


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
    chip.use(zafg1um)

    if part_name not in chip.getkeys('fpga'):
        chip.error(f'{part_name} has not been loaded', fatal=True)

    # 3. Load flow
    chip.use(ebrick_fpga_flow)

    # 4. Setup default show tools
    utils.set_common_showtools(chip)

    # 5. Select default flow
    chip.set('option', 'mode', 'fpga', clobber=False)
    chip.set('option', 'flow', 'ebrick_fpga_flow', clobber=False)


#########################
if __name__ == "__main__":
    target = siliconcompiler.Chip('<target>')
    setup(target)
    target.write_manifest('zafg1um_target.json')
