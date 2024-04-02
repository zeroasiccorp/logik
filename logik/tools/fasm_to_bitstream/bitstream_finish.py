##############################################################################
# Copyright 2024 Zero ASIC Corporation
#
# Licensed under the MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY,WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ----
#
##############################################################################

from logik.tools.fasm_to_bitstream import \
    fasm_to_bitstream as fasm_utils


def setup(chip):
    '''
    Perform bitstream finishing
    '''

    tool = 'fasm_to_bitstream'
    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    task = chip._get_task(step, index)

    part_name = chip.get('fpga', 'partname')

    # Require that a lut size is set for FPGA scripts.
    chip.add('tool', tool, 'task', task, 'require',
             ",".join(['fpga', part_name, 'file', 'bitstream_map']),
             step=step, index=index)


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
        chip.error("fasm_to_bitstream requires a bitstream map file",
                   fatal=True)
    else:
        chip.error("Only one bitstream map file can be passed to fasm_to_bitstream.py", fatal=True)

    return 0
