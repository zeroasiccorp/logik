
import argparse
import os

import siliconcompiler
import ebrick_fpga_cad

from ebrick_fpga_cad.targets import fpga_zeta_target
from ebrick_fpga_cad.targets import zafg1um_target


def main(part_name='zafg1um_0202'):

    top_module = 'fir_filter_wrapper'
    
    chip = siliconcompiler.Chip(f'{top_module}')

    #chip.set('fpga', 'partname', 'fpga_zeta_demo')
    chip.set('fpga', 'partname', part_name)

    # 1. Defining the project

    # 2. Define source files
    src_path = "../rtl"
    src_files = [
        "tree_adder.v",
        "fir_filter.v",
        "fir_filter_wrapper.v",
    ]
    
    for filename in src_files :
        chip.input(os.path.join(src_path, filename))

    # 3. Load target
    #chip.load_target(fpga_zeta_target)
    chip.load_target(zafg1um_target)

    # 4. Customize steps for this design
    chip.add('option', 'define', 'FIR_FILTER_CONSTANT_COEFFS')
    
    chip.run()


if __name__ == "__main__":
    option_parser = argparse.ArgumentParser("ebrick-fpga CAD FIR Filter Demo")
    option_parser.add_argument("-part_name", default="zafg1um_0202")
    options = option_parser.parse_args()
    main(part_name=options.part_name)
