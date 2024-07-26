# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from logik.tools.fasm_to_bitstream import \
    fasm_to_bitstream as fasm_utils
from siliconcompiler.tools._common import get_tool_task
from siliconcompiler import SiliconCompilerError


def setup(chip):
    '''
    Perform bitstream finishing
    '''

    tool = 'fasm_to_bitstream'
    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    _, task = get_tool_task(chip, step, index)

    part_name = chip.get('fpga', 'partname')

    # Require that a lut size is set for FPGA scripts.
    chip.add('tool', tool, 'task', task, 'require',
             ",".join(['fpga', part_name, 'file', 'bitstream_map']),
             step=step, index=index)

    chip.add('tool', tool, 'task', task, 'input', f'{chip.top()}.fasm', step=step, index=index)
    chip.add('tool', tool, 'task', task, 'output', f'{chip.top()}.json', step=step, index=index)
    chip.add('tool', tool, 'task', task, 'output', f'{chip.top()}.bin', step=step, index=index)


def run(chip):
    part_name = chip.get('fpga', 'partname')

    topmodule = chip.top()
    fasm_file = f"inputs/{topmodule}.fasm"

    bitstream_maps = chip.find_files('fpga', part_name, 'file', 'bitstream_map')

    if len(bitstream_maps) == 1:
        json_outfile = f"outputs/{topmodule}.json"
        binary_outfile = f"outputs/{topmodule}.bin"

        # Finishing steps are as follows:
        # 1. Convert FASM to IR
        config_bitstream = fasm_utils.fasm2bitstream(fasm_file, bitstream_maps[0])

        # 2.  Write IR to JSON for inspection purposes
        fasm_utils.write_bitstream_json(config_bitstream, json_outfile)

        # 3.  Flatten the IR to a 1D address space
        flattened_bitstream = fasm_utils.generate_flattened_bitstream(config_bitstream)

        # 4.  Format the flattened bitstream to binary
        binary_bitstream = fasm_utils.format_binary_bitstream(flattened_bitstream)

        # 5.  Write binary to file
        fasm_utils.write_bitstream_binary(binary_bitstream, binary_outfile)

    elif len(bitstream_maps) == 0:
        raise SiliconCompilerError(
            "fasm_to_bitstream requires a bitstream map file", chip=chip)
    else:
        raise SiliconCompilerError(
            "Only one bitstream map file can be passed to fasm_to_bitstream", chip=chip)

    return 0
