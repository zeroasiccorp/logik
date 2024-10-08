#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler import Chip
from logik.targets import logik_target


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
    chip.set('fpga', 'partname', 'logik_demo')

    # Load target settings
    chip.use(logik_target)

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()


if __name__ == "__main__":
    hello_adder()
