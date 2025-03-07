# eth_mac_1g.py

# This is the logik run script for demonstrating RTL-to-bitstream
# with Alex Forencich's 1G Ethnernet MAC

import os

from siliconcompiler import Chip
from logik.targets import logik_target


def build():

    design_name = 'eth_mac_1g'

    part_name = 'z1000'

    chip = Chip(f'{design_name}')

    # Set default part name
    chip.set('fpga', 'partname', part_name)

    # Logik has a generic Silicon Compiler target that
    # the part driver plugs into, so we need to use that
    chip.use(logik_target)

    # Define source files from verilog-ethernet repo

    # First we need to register the verilog-ethernet repo
    # as a package
    chip.register_source(
        name='verilog-ethernet',
        path='git+https://github.com/alexforencich/verilog-ethernet.git',
        ref='main')

    # Then we can pull in the specific RTL we need from that
    # repository -- Silicon Compiler will download and cache the files
    # for us
    design_source_files = get_source_files()
    for source_file in design_source_files:
        source_path = f'rtl/{source_file}'
        chip.input(source_path, package='verilog-ethernet')

    # Add in our top-level wrapper, stored locally
    chip.input('eth_mac_1g_wrapper.v')

    # Set the top module
    chip.set('option', 'entrypoint', 'eth_mac_1g_wrapper')

    # Add timing constraints
    chip.input(os.path.join(os.getcwd(), f'{design_name}.sdc'))

    # Define pin constraints
    chip.input(os.path.join(os.getcwd(), f'constraints/{part_name}/pin_constraints.pcf'))

    # Customize steps for this design

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


def get_source_files():

    return [
        'eth_mac_1g.v',
        'axis_gmii_rx.v',
        'axis_gmii_tx.v',
        'lfsr.v'
    ]


if (__name__ == '__main__'):
    build()
