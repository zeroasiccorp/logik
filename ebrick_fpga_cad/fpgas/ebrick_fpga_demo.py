import os
import siliconcompiler
from ebrick_fpga_cad.fpgas import _common


####################################################
# Setup for ebrick_fpga_demo Family FPGAs
####################################################
def setup(chip):
    '''
    The ebrick_fpga_demo FPGA family is a set of
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
        'ebrick_fpga_demo',
    ]

    # Settings common to all parts in family
    for part_name in all_part_names:

        # Assemble the name of the CAD release to obtain
        # from github

        current_release = 'v0.1.8'
        cad_part_release_url = _common.get_efpga_release_url(
            current_release,
            f'{part_name}_cad.tar.gz')
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

        _common.set_fpga_resources(fpga)

        if part_name == 'ebrick_fpga_demo':
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

            bitstream_map_file = os.path.join(cad_root, 'ebrick_fpga_core_bitstream_map.json')
            fpga.set('fpga', part_name, 'file', 'bitstream_map', bitstream_map_file)

            gasket_map_file = os.path.join(cad_root, f'{part_name}_gasket_map.json')
            fpga.set('fpga', part_name, 'file', 'gasket_map', gasket_map_file)

            fpga.set('fpga', part_name, 'var', 'channelwidth', '136')

        all_fpgas.append(fpga)

    return all_fpgas


#########################
if __name__ == "__main__":
    for fpga in setup(siliconcompiler.Chip('<fpga>')):
        fpga.write_manifest(f'{fpga.design}.json')
