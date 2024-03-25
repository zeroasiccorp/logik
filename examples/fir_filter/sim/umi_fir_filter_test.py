#!/usr/bin/env python3
# umi_fir_filter_test.py

# Copyright (c) 2024 Zero ASIC Corporation
# This code is licensed under Apache License 2.0 (see LICENSE for details)

import numpy as np

from switchboard import SbDut
from switchboard import UmiTxRx
from switchboard import delete_queue

import lambdalib
import umi

from generate_vectors import generate_fir_filter_vectors


def run_test(trace=False, fast=False):
    ############################
    # build the RTL simulation #
    ############################

    print('*** Building the RTL simulation ***')

    # SbDut is a subclass of siliconcompiler.Chip, with some extra
    # options and features geared towards simulation with switchboard.
    #
    # Here's what the constructor arguments mean:
    # * 'umi_fir_filter_test' is the name of the top-level module
    # * 'tool' indicates the Verilog simulation tool ('verilator' or 'icarus')
    # * 'trace' indicates whether waveforms should be dumped
    # * 'default_main' is Verilator-specific; when True indicats that
    #   switchboard's default C++ main() implementation should be used.
    #   this testbench has its own main; so we set it to False

    dut = SbDut('testbench', tool='verilator', trace=trace, default_main=True)

    # The next few commands specify the Verilog sources to be used in the
    # simulation.

    # import the UMI library
    dut.use(umi)
    dut.add('option', 'library', 'umi')

    # import lambdalib
    dut.use(lambdalib)
    dut.add('option', 'library', 'lambdalib_stdlib')

    # Add this repo as a package source
    dut.register_package_source(
        name='umi_fir_filter',
        path='git+https://github.com/zeroasiccorp/ebrick-fpga-cad.git',
        ref='umi_fir_filter')

    dut.input('examples/fir_filter/rtl/fir_filter.v', package='umi_fir_filter')
    dut.input('examples/fir_filter/rtl/tree_adder.v', package='umi_fir_filter')
    dut.input('examples/fir_filter/rtl/umi_fir_filter.v', package='umi_fir_filter')
    dut.input('examples/fir_filter/rtl/umi_fir_filter_regs.v', package='umi_fir_filter')

    dut.input('examples/fir_filter/sim/testbench.sv', package='umi_fir_filter')

    # Setup all the needed compiler directives

    dut.add('option', 'define', 'FIR_FILTER_CONSTANT_COEFFS')
    dut.add('option', 'define', 'VECTOR_COUNT_MAX=100')

    # Set include directories
    dut.add('option', 'idir', 'examples/fir_filter/rtl', package='umi_fir_filter')

    # build() kicks off the simulator build using the source files configured
    # in the previous commands. The result depends on the simulator being used
    # For Verilator, the output of build() is an executable that can be run
    # in a standalone fashion, while for Icarus Verilog, the result is a binary
    # run with vvp. The "fast" argument indicates whether the build should be
    # skipped if the binary output already exists.

    dut.build(fast=fast)

    #############################
    # create switchboard queues #
    #############################

    print('*** Creating switchboard queues ***')

    # These commands create new switchboard queues that will show up
    # as files in the file system. The queue names must match the
    # names used on the Verilog side in testbench.sv. This is somewhat
    # similar to specifying TCP ports to be used on two sides of a
    # connection.

    umi_queues = setup_queues()

    #############################
    # launch the RTL simulation #
    #############################

    print('*** Launching RTL simulation ***')

    # simulate() launches the RTL simulation built earlier via the build() command

    dut.simulate()

    # Generate the fir filter vectors
    generate_fir_filter_vectors(16, 100)

    device = UmiTxRx(umi_queues['client2rtl'], umi_queues['rtl2client'])
    # host = UmiTxRx(umi_queues['host2rtl'], umi_queues['rtl2host'])

    input_vectors = load_binary_data("fir_filter_input_vectors.dat")
    expected_output = load_binary_data("fir_filter_output_vectors.dat")

    coeffs = [
        0x0001,
        0x0002,
        0x0004,
        0x0008,
        0x0008,
        0x0004,
        0x0002,
        0x0001,
    ]

    print("INFO:  Load coefficients")
    device.write(0x0000000000000010, np.array(coeffs, dtype='uint16'), posted=True)

    print("INFO:  Generate samples")
    for i in range(len(input_vectors)):
        device.write(0x0000000000000020, input_vectors[i])

    print("INFO:  Read back samples")
    filter_output = []
    for i in range(len(input_vectors)):
        filter_output.append(device.read(0x0000000000000030 + (64 * i), np.uint64))

    print("INFO:  Check outputs")
    errors = 0
    for i in range(len(filter_output)):
        if (expected_output[i] != filter_output[i]):
            print(f"ERROR {i}: expected {hex(expected_output[i])} got {hex(filter_output[i])}")
            errors += 1

    print(f"ERRORS = {errors}")
    if (errors == 0):
        print("PASS")
    else:
        print("FAIL")


def load_binary_data(datafile):

    binary_data = []

    with open(datafile, "r") as bin_data:
        for data_entry in bin_data.readlines():
            binary_data.append(int(data_entry, base=2))

    bin_data.close()

    return np.array(binary_data, dtype='uint64')


def setup_queues(client2rtl="client2rtl.q",
                 rtl2client="rtl2client.q",
                 host2rtl="host2rtl.q",
                 rtl2host="rtl2host.q"):

    # clean up old queues if present
    for q in [client2rtl, rtl2client, host2rtl, rtl2host]:
        delete_queue(q)

    all_queues = {"client2rtl": client2rtl,
                  "rtl2client": rtl2client,
                  "host2rtl": host2rtl,
                  "rtl2host": rtl2host}

    return all_queues


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--fast', action='store_true',
        help="don't build the simulator if one is found")
    parser.add_argument('--trace', action='store_true',
        help="dump waveforms during simulation")

    args = parser.parse_args()

    run_test(trace=args.trace, fast=args.fast)
