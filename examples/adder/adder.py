#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler import Chip
from logik.flows import logik_flow
from logiklib.demo.example_arch_X005Y005 import example_arch_X005Y005
from logiklib.demo.example_arch_X008Y008 import example_arch_X008Y008
from logiklib.demo.example_arch_X014Y014 import example_arch_X014Y014
from logiklib.demo.example_arch_X030Y030 import example_arch_X030Y030
from logiklib.demo.logik_demo import logik_demo


def hello_adder(part_name='logik_demo'):

    # Create compilation object
    chip = Chip('adder')

    # Specify design sources
    chip.input('adder.v')

    # Specify pin constraints
    chip.input('adder.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)

    # Select target fpga
    chip.set('fpga', 'partname', part_name)

    chip.set('option', 'builddir', f'adder_{part_name}')

    # Load target settings
    chip.set('option', 'flow', 'logik_flow')
    chip.use(logik_flow)
    # Only use the part you're planning to use; otherwise
    # all the CAD tarballs get downloaded
    if (part_name == 'example_arch_X005Y005'):
        chip.use(example_arch_X005Y005)
    elif (part_name == 'example_arch_X008Y008'):
        chip.use(example_arch_X008Y008)
    elif (part_name == 'example_arch_X014Y014'):
        chip.use(example_arch_X014Y014)
    elif (part_name == 'example_arch_X030Y030'):
        chip.use(example_arch_X030Y030)
    elif (part_name == 'logik_demo'):
        chip.use(logik_demo)
    else:
        raise ValueError(f"Unsupported part name {part_name}")

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()


if __name__ == "__main__":
    hello_adder()
