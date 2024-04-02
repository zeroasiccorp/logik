###############################################################################
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

from siliconcompiler import Flow, Chip
from siliconcompiler.flows._common import setup_frontend

from siliconcompiler.tools.yosys import syn_fpga as yosys_syn
from siliconcompiler.tools.vpr import place as vpr_place
from siliconcompiler.tools.vpr import route as vpr_route
from siliconcompiler.tools.genfasm import bitstream as genfasm_bitstream

from logik.tools.fasm_to_bitstream import bitstream_finish
from logik.tools.generate_vpr_constraints import constraint_gen


############################################################################
# DOCS
############################################################################
def make_docs(chip):
    return setup(chip)


############################################################################
# Flowgraph Setup
############################################################################
def setup(chip, flowname='logik_flow'):
    '''
    '''

    flow = Flow(chip, flowname)

    flow_pipe = [
        ('syn', yosys_syn),
        ('place', vpr_place),
        ('route', vpr_route),
        ('genfasm', genfasm_bitstream),
        ('bitstream', bitstream_finish),
    ]

    flowtools = setup_frontend(chip)
    flowtools.extend(flow_pipe)

    # Minimal setup
    index = '0'
    prevstep = None
    for step, tool_module in flowtools:
        # Flow
        flow.node(flowname, step, tool_module)
        if prevstep:
            flow.edge(flowname, prevstep, step)
        # Hard goals
        for metric in ('errors', 'warnings', 'drvs', 'unconstrained',
                       'holdwns', 'holdtns', 'holdpaths',
                       'setupwns', 'setuptns', 'setuppaths'):
            flow.set('flowgraph', flowname, step, index, 'goal', metric, 0)
        # Metrics
        for metric in ('luts', 'dsps', 'brams', 'registers', 'pins'):
            flow.set('flowgraph', flowname, step, index, 'weight', metric, 1.0)
        prevstep = step

    flow.node(flowname, 'constraint_gen', constraint_gen)
    flow.edge(flowname, 'constraint_gen', 'place')

    return flow


##################################################
if __name__ == "__main__":
    flow = make_docs(Chip('<flow>'))
    flow.write_flowgraph(f"{flow.top()}.png", flow=flow.top())
