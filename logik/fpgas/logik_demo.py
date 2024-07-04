# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import os
from siliconcompiler import FPGA, Chip
from logik.fpgas import _common


####################################################
# Setup for logik_demo Family FPGAs
####################################################
def setup(chip):
    '''
    The logik_demo FPGA family is a set of
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

    vendor = 'zeroasic'

    lut_size = 4

    all_fpgas = []

    all_part_names = [
        'logik_demo',
        'logik_demo_mini',
    ]

    # Settings common to all parts in family
    for part_name in all_part_names:
        fpga = FPGA(chip, part_name, package=_common.get_package_name(part_name))
        fpga.register_source(
            _common.get_package_name(part_name),
            path=_common.get_download_url(part_name),
            ref=_common.fpga_version)

        fpga.set('fpga', part_name, 'vendor', vendor)

        fpga.set('fpga', part_name, 'lutsize', lut_size)
        fpga.add('fpga', part_name, 'var', 'feature_set', 'async_reset')
        fpga.add('fpga', part_name, 'var', 'feature_set', 'async_set')
        fpga.add('fpga', part_name, 'var', 'feature_set', 'enable')

        fpga.add('fpga', part_name, 'var', 'vpr_clock_model', 'route')

        cad_root = os.path.join(f'{part_name}_cad', 'cad')
        fpga.set('fpga', part_name, 'file', 'archfile',
                 os.path.join(cad_root, 'logik_demo_core.xml'))
        fpga.set('fpga', part_name, 'file', 'graphfile',
                 os.path.join(cad_root, 'logik_demo_core_rr_graph.xml'))

        _common.set_fpga_resources(fpga)

        if ((part_name == 'logik_demo') or (part_name == 'logik_demo_mini')):
            techlib_root = os.path.join(f'{part_name}_cad', 'techlib')

            flop_library = os.path.join(techlib_root, 'tech_flops.v')
            fpga.set('fpga', part_name, 'file', 'yosys_flop_techmap', flop_library)

            bram_library = os.path.join(techlib_root, 'tech_bram.v')
            fpga.set('fpga', part_name, 'file', 'yosys_memory_techmap', bram_library)

            bram_memmap = os.path.join(techlib_root, 'bram_memory_map.txt')
            fpga.set('fpga', part_name, 'file', 'yosys_memory_libmap', bram_memmap)

            dsp_library = os.path.join(techlib_root, 'tech_dsp.v')
            fpga.set('fpga', part_name, 'file', 'yosys_dsp_techmap', dsp_library)

            mae_library = os.path.join(techlib_root, 'tech_mae.v')
            fpga.add('fpga', part_name, 'file', 'yosys_extractlib', mae_library)
            fpga.add('fpga', part_name, 'file', 'yosys_macrolib', mae_library)

            # Set the dsp options for the yosys built-in DSP correctly for this
            # architecture
            fpga.add('fpga', part_name, 'var', 'yosys_dsp_options', 'DSP_A_MAXWIDTH=18')
            fpga.add('fpga', part_name, 'var', 'yosys_dsp_options', 'DSP_B_MAXWIDTH=18')
            fpga.add('fpga', part_name, 'var', 'yosys_dsp_options', 'DSP_A_MINWIDTH=2')
            fpga.add('fpga', part_name, 'var', 'yosys_dsp_options', 'DSP_B_MINWIDTH=2')
            fpga.add('fpga', part_name, 'var', 'yosys_dsp_options', 'DSP_NAME=_dsp_block_')

            fpga.add('fpga', part_name, 'var', 'dsp_blackbox_options', 'BLACKBOX_MACROS')

            bitstream_map_file = os.path.join(cad_root, 'logik_demo_core_bitstream_map.json')
            fpga.set('fpga', part_name, 'file', 'bitstream_map', bitstream_map_file)

            constraint_map_file = os.path.join(cad_root, f'{part_name}_constraint_map.json')
            fpga.set('fpga', part_name, 'file', 'constraints_map', constraint_map_file)

            if (part_name == 'logik_demo'):
                fpga.set('fpga', part_name, 'var', 'channelwidth', '136')
            elif (part_name == 'logik_demo_mini'):
                fpga.set('fpga', part_name, 'var', 'channelwidth', '136')

        all_fpgas.append(fpga)

    return all_fpgas


#########################
if __name__ == "__main__":
    for fpga in setup(Chip('<fpga>')):
        fpga.write_manifest(f'{fpga.design}.json')
