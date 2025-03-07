#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler import Chip
from logik.flows import logik_flow
from logiklib.demo.logik_demo import logik_demo


def umi_hello():

    # Create compilation object
    chip = Chip('umi_hello')
    chip.create_cmdline(switchlist=['-remote'])

    # Specify Design sources
    chip.input('umi_hello.v')

    # Specify pin constraints
    chip.input('umi_hello.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)

    # Select target fpga
    chip.set('fpga', 'partname', 'logik_demo')

    # Load target settings
    chip.set('option', 'flow', 'logik_flow')
    chip.use(logik_flow)
    chip.use(logik_demo)

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()


if __name__ == "__main__":
    umi_hello()
