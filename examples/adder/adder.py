#!/usr/bin/env python3

from siliconcompiler import Chip
from logik.targets import logik_target


def hello_adder():

    # Create compilation object
    chip = Chip('adder')

    # Specify Design sources
    chip.input('adder.v')

    # Specify pin constraints
    chip.input('adder.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)
    # chip.set('option', 'remote', True)

    # Select target fpga
    chip.set('fpga', 'partname', 'logik_demo')

    # Load target settings
    chip.load_target(logik_target)

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()


if __name__ == "__main__":
    hello_adder()
