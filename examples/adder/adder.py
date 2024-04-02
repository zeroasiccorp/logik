#!/usr/bin/env python3

from siliconcompiler import Chip
from logik.targets import logik_target


def hello_adder():

    # Create compilation object
    chip = Chip('adder')

    # Specify Design sources
    chip.input('adder.v')

    # Specify pin constraints
    # chip.input('adder.pcf')
    chip.add('input', 'constraint', 'pinmap', 'adder.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)
    # chip.set('option', 'remote', True)

    # Select target fpga
    chip.set('fpga', 'partname', 'logik_demo')

<<<<<<< HEAD
    # Load target settings
=======
    # 2. Define source files
    project_path = os.path.abspath(os.path.dirname(__file__))
    chip.input(os.path.join(project_path, 'rtl', 'adder.v'))

    # 3. Define constraints
    chip.input(os.path.join(project_path, 'constraints', f'pin_constraints_{set_part_name}.pcf'))

    # 3. Load target
>>>>>>> main
    chip.load_target(logik_target)

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()


if __name__ == "__main__":
    hello_adder()
