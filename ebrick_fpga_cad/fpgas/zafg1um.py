#zafg1um.py

import os
import siliconcompiler


####################################################
# Setup for zafg1um Family FPGAs
####################################################
def setup(chip):
    '''
    The zafg1um FPGA family is a set of
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
    
    flow_root = os.path.join(ROOTDIR.replace("ebrick_fpga_cad/fpgas/zafg1um.py", "examples"),
                             'ebrick-fpga')
    
    vendor = 'N/A'

    lut_size = '4'
    flop_async_set = '1'
    flop_async_reset = '1'
    flop_enable = '1'
    
    all_fpgas = []

    all_part_names = [
        'zafg1um_0202',
    ]

    # Settings common to all parts in family
    for part_name in all_part_names:

        fpga = siliconcompiler.FPGA(chip, part_name)

        chip.register_package_source('ebrick_fpga', flow_root)
        
        fpga.set('fpga', part_name, 'vendor', vendor)

        fpga.set('fpga', part_name, 'lutsize', lut_size)
        fpga.set('fpga', part_name, 'var', 'feature_set', 'async_set')
        fpga.set('fpga', part_name, 'var', 'feature_set', 'async_reset')
        fpga.set('fpga', part_name, 'var', 'feature_set', 'enable')

        arch_root = os.path.join(flow_root, part_name, 'cad')
        fpga.set('fpga', part_name, 'file', 'archfile',
                 os.path.join(arch_root, 'ebrick_fpga_core.xml'))
        fpga.set('fpga', part_name, 'file', 'graphfile',
                 os.path.join(arch_root, 'ebrick_fpga_core_rr_graph.xml'))

        if (part_name == 'zafg1um_0202'): 
            flop_library = os.path.join(flow_root, part_name, 'techlib', 'ebrick_fpga_tech_flops.v')
            fpga.set('fpga', part_name, 'file', 'yosys_flop_techmap', flop_library)
            
            bitstream_map_file = os.path.join(arch_root, 'ebrick_fpga_core_bitstream_map.json')
            fpga.set('fpga', part_name, 'file', 'bitstream_map', bitstream_map_file)
            
            fpga.set('fpga', part_name, 'var', 'channelwidth', '136')

        all_fpgas.append(fpga)

    return all_fpgas


#########################
if __name__ == "__main__":
    for fpga in setup(siliconcompiler.Chip('<fpga>')):
        fpga.write_manifest(f'{fpga.design}.json')
