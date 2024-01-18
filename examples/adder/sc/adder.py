
import argparse
import os

import siliconcompiler
import ebrick_fpga_cad

from ebrick_fpga_cad.targets import ebrick_fpga_target


def main(part_name='zafg1um_0202'):

    top_module = 'adder'
    
    chip = siliconcompiler.Chip(f'{top_module}')

    chip.set('fpga', 'partname', part_name)

    # 1. Defining the project

    # 2. Define source files
    src_path = os.path.abspath(__file__).replace('sc/adder.py','rtl')
    src_files = [
        "adder.v",
    ]
    
    for filename in src_files :
        chip.input(os.path.join(src_path, filename))

    # 3. Load target
    chip.load_target(ebrick_fpga_target)

    chip.run()


if __name__ == "__main__":
    option_parser = argparse.ArgumentParser("ebrick-fpga CAD adder Demo")
    option_parser.add_argument("-part_name", default="zafg1um_0202")
    options = option_parser.parse_args()
    main(part_name=options.part_name)
