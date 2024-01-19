#zafg00um.py

import os
import siliconcompiler


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
    
    flow_root = ROOTDIR.replace("ebrick_fpga_cad/fpgas/zafg00um.py",
                                "examples")
    
    vendor = 'N/A'

    lut_size = '4'
    
    all_fpgas = []

    all_part_names = [
        'zafg00um_0202',
    ]

    # Settings common to all parts in family
    for part_name in all_part_names:

        fpga = siliconcompiler.FPGA(chip, part_name)

        fpga.set('fpga', part_name, 'vendor', vendor)

        fpga.set('fpga', part_name, 'lutsize', lut_size)
        #***TO DO:  Put these back in when a newer version of this arch
        #           is being tested
        #fpga.add('fpga', part_name, 'var', 'feature_set', 'async_reset')
        #fpga.add('fpga', part_name, 'var', 'feature_set', 'async_set')
        #fpga.add('fpga', part_name, 'var', 'feature_set', 'enable')

        arch_root = os.path.join(flow_root, 'ebrick-fpga', part_name, 'cad')
        fpga.set('fpga', part_name, 'file', 'archfile',
                 os.path.join(arch_root, 'ebrick_fpga_core.xml'))
        fpga.set('fpga', part_name, 'file', 'graphfile',
                 os.path.join(arch_root, 'ebrick_fpga_core_rr_graph.xml'))

        if (part_name == 'zafg00um_0202'):
            #***TO DO:  Put these back in when a newer version of this arch
            #           is being tested
            #flop_library = os.path.join(flow_root, 'ebrick-fpga', part_name, 'techlib', 'ebrick_fpga_tech_flops.v')
            #fpga.set('fpga', part_name, 'file', 'yosys_flop_techmap', flop_library)
            
            bitstream_map_file = os.path.join(arch_root, 'ebrick_fpga_core_bitstream_map.json')
            fpga.set('fpga', part_name, 'file', 'bitstream_map', bitstream_map_file)
            
            fpga.set('fpga', part_name, 'var', 'channelwidth', '128')

        all_fpgas.append(fpga)

    return all_fpgas


#########################
if __name__ == "__main__":
    for fpga in setup(siliconcompiler.Chip('<fpga>')):
        fpga.write_manifest(f'{fpga.design}.json')
