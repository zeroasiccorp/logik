#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler import Chip
from logik.targets import logik_target


def umi_hello(remote=False):

    # Create compilation object
    chip = Chip('umi_hello')

    # Specify Design sources
    chip.input('umi_hello.v')

    # Specify pin constraints
    chip.input('umi_hello.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)
    chip.set('option', 'remote', remote)

    # Select target fpga
    chip.set('fpga', 'partname', 'logik_demo')

    # Load target settings
    chip.load_target(logik_target)

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-remote', action='store_true',
        help='Build bitstream in the cloud instead of using local tools.')
    args = parser.parse_args()

    umi_hello(remote=args.remote)
