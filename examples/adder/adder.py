#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler import Chip
from logik.flows import logik_flow
from logiklib.demo.K4_N8_6x6 import K4_N8_6x6


def hello_adder():

    # Create compilation object
    chip = Chip('adder')
    chip.create_cmdline(switchlist=['-remote'])

    # Specify design sources
    chip.input('adder.v')

    # Specify pin constraints
    chip.input('adder.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)

    # Select target fpga
    chip.set('fpga', 'partname', 'K4_N8_6x6')

    # Load target settings
    chip.set('option', 'flow', 'logik_flow')
    chip.use(logik_flow)
    chip.use(K4_N8_6x6)

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()


if __name__ == "__main__":
    hello_adder()
