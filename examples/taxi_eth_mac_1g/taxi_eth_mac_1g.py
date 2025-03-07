# eth_mac_1g.py

# This is the logik run script for demonstrating RTL-to-bitstream
# with Alex Forencich's 1G Ethernet MAC

import os

from siliconcompiler import Chip
from logik.targets import logik_target


def build():

    design_name = 'taxi_eth_mac_1g'

    part_name = 'logik_demo'

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
        name='verilog-ethernet-taxi',
        path='git+https://github.com/fpganinja/taxi.git',
        ref='main')

    # Then we can pull in the specific RTL we need from that
    # repository -- Silicon Compiler will download and cache the files
    # for us
    design_source_files = get_source_files()
    for source_file in design_source_files:
        source_path = f'rtl/{source_file}'
        chip.input(source_path, package='verilog-ethernet-taxi')

    # Add in our top-level wrapper, stored locally
    chip.input('taxi_eth_mac_1g_wrapper.sv')
    
    # Set the top module
    chip.set('option', 'entrypoint', 'taxi_eth_mac_1g_wrapper')

    # Add timing constraints
    chip.input(os.path.join(os.getcwd(), f'{design_name}.sdc'))

    # Define pin constraints
    chip.input(os.path.join(os.getcwd(), f'{design_name}_pin_constraints.pcf'))

    # Customize steps for this design

    # Set to use SystemVerilog front end
    # chip.set('option', 'frontend', 'systemverilog')
    
    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


def get_source_files():

    return [
        'axis/taxi_axis_if.sv',
        'eth/taxi_eth_mac_1g.sv',
        'eth/taxi_axis_gmii_rx.sv',
        'eth/taxi_axis_gmii_tx.sv',
        'lfsr/taxi_lfsr.sv'
    ]


if (__name__ == '__main__'):
    build()
