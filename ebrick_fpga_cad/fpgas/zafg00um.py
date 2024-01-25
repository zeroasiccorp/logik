#zafg00um.py

import os
import siliconcompiler
from ebrick_fpga_cad.fpgas import _common


####################################################
# Setup for zafg00um Family FPGAs
####################################################
def setup(chip):
    '''
    The zafg00um FPGA family is a set of
    open source architectures used as illustrative
    examples for academic FPGA architectures.  They
    are based on numerous examples furnished over the
    the years by the University of Toronto with different
    distributions of VPR

    For more information about VPR and its architecture models,
    see Murray et. al, "VTR 8: High Performance CAD and Customizable
    FPGA Architecture Modelling", ACM Trans. Reconfigurable Technol.
    Syst., 2020, https://www.eecg.utoronto.ca/~kmurray/vtr/vtr8_trets.pdf
    '''

    ROOTDIR = os.path.abspath(__file__)
    
    vendor = 'zeroasic'

    lut_size = '4'
    
    all_fpgas = []

    all_part_names = [
        'zafg00um_0202',
    ]

    # Settings common to all parts in family
    for part_name in all_part_names:

        # Assemble the name of the CAD release to obtain
        # from github

        current_release = 'v0.5.13'
        cad_part_release_url = _common.get_release_url(current_release, f'ebrick-fpga_{part_name}_cad.tar.gz')
        chip.register_package_source(name=f'ebrick_fpga-{part_name}',
                                     path=cad_part_release_url,
                                     ref=current_release)

        fpga = siliconcompiler.FPGA(chip, part_name, package=f'ebrick_fpga-{part_name}')

        fpga.set('fpga', part_name, 'vendor', vendor)

        fpga.set('fpga', part_name, 'lutsize', lut_size)
        fpga.add('fpga', part_name, 'var', 'feature_set', 'async_reset')
        fpga.add('fpga', part_name, 'var', 'feature_set', 'async_set')
        fpga.add('fpga', part_name, 'var', 'feature_set', 'enable')

        cad_root = os.path.join(f'{part_name}_cad', 'cad')
        fpga.set('fpga', part_name, 'file', 'archfile',
                 os.path.join(cad_root, 'ebrick_fpga_core.xml'))
        fpga.set('fpga', part_name, 'file', 'graphfile',
                 os.path.join(cad_root, 'ebrick_fpga_core_rr_graph.xml'))

        if (part_name == 'zafg00um_0202'):
            
            techlib_root = os.path.join(f'{part_name}_cad', 'techlib')
            
            flop_library = os.path.join(techlib_root, 'ebrick_fpga_tech_flops.v')
            fpga.set('fpga', part_name, 'file', 'yosys_flop_techmap', flop_library)
            
            bitstream_map_file = os.path.join(cad_root, 'ebrick_fpga_core_bitstream_map.json')
            fpga.set('fpga', part_name, 'file', 'bitstream_map', bitstream_map_file)
            
            fpga.set('fpga', part_name, 'var', 'channelwidth', '128')

        all_fpgas.append(fpga)

    return all_fpgas


#########################
if __name__ == "__main__":
    for fpga in setup(siliconcompiler.Chip('<fpga>')):
        fpga.write_manifest(f'{fpga.design}.json')
