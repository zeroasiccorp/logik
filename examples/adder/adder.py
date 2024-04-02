#!/usr/bin/env python3

from siliconcompiler import Chip
from logik.targets import logik_target

def hello_adder():

    # Create compilation object
    chip = Chip('adder')                                   # Specify top module

    # User Settings
    chip.input('adder.v')                                  # Define source files
    chip.input('adder.pcf')                                # Define source files
    chip.set('option', 'quiet', True)                      # Quite compiler mode

    # Select Flow and Part name
    chip.set('fpga', 'partname', 'logik_demo')             # Set FPGA part name
    chip.load_target(logik_target)                         # Load flow/part target

    # Run Compiler
    chip.run()

    # Gather Compiler Metrics
    chip.summary()

if __name__ == "__main__":
    hello_adder()
