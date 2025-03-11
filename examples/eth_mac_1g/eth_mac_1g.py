#!/usr/bin/env python3

# This is the logik run script for demonstrating RTL-to-bitstream
# with Alex Forencich's 1G Ethernet MAC

from siliconcompiler import Chip
from logik.flows import logik_flow
from logiklib.demo.logik_demo import logik_demo


def build(part='logik_demo'):
    chip = Chip('eth_mac_1g_wrapper')

    # Load target settings
    chip.use(logik_flow)
    chip.use(logik_demo)
    chip.set('option', 'flow', 'logik_flow')

    # Set default part name
    chip.set('fpga', 'partname', part)

    # Define source files from verilog-ethernet repo

    # First we need to register the verilog-ethernet repo
    # as a package
    chip.register_source(
        name='verilog-ethernet',
        path='git+https://github.com/alexforencich/verilog-ethernet.git',
        ref='77320a9471d19c7dd383914bc049e02d9f4f1ffb')

    # Then we can pull in the specific RTL we need from that
    # repository -- Silicon Compiler will download and cache the files
    # for us
    for source_file in ('eth_mac_1g.v',
                        'axis_gmii_rx.v',
                        'axis_gmii_tx.v',
                        'lfsr.v'):
        chip.input(f'rtl/{source_file}', package='verilog-ethernet')

    # Add in our top-level wrapper, stored locally
    chip.register_source('ethmac_example', __file__)
    chip.input('eth_mac_1g_wrapper.v', package='ethmac_example')

    # Add timing constraints
    chip.input('eth_mac_1g.sdc', package='ethmac_example')

    # Define pin constraints
    chip.input(f"constraints/{chip.get('fpga', 'partname')}/pin_constraints.pcf",
               package='ethmac_example')

    # Customize steps for this design
    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if __name__ == '__main__':
    build()
