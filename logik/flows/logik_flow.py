# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler import Chip
from siliconcompiler.flows import fpgaflow

from logik.tools.fasm_to_bitstream import bitstream_finish


############################################################################
# DOCS
############################################################################
def make_docs(chip):
    return setup()


############################################################################
# Flowgraph Setup
############################################################################
def setup(flowname='logik_flow'):
    '''
    '''

    flow = fpgaflow.setup(
        flowname=flowname,
        fpgaflow_type='vpr')

    # Add bitstream generation task
    flow.node(flowname, 'convert_bitstream', bitstream_finish)
    flow.edge(flowname, 'bitstream', 'convert_bitstream')

    return flow


##################################################
if __name__ == "__main__":
    flow = make_docs(Chip('<flow>'))
    flow.write_flowgraph(f"{flow.top()}.png", flow=flow.top(), landscape=True)
