# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

fpga_version = 'v0.1.22'


def get_package_name(part_name):
    return f"logik-fpga-{part_name}"


def get_download_url(part_name):
    root = "https://github.com/zeroasiccorp/logik/releases/download"
    return f"{root}/fpga-{fpga_version}/{part_name}_cad.tar.gz"


def set_fpga_resources(fpga):
    part_name = fpga.design

    for tool in ('vpr', 'yosys'):
        fpga.add('fpga', part_name, 'var', f'{tool}_registers', [
            'dff',
            'dffr',
            'dffs',
            'dffe',
            'dffer',
            'dffes',
            'dffrs',
            'dffers'])
        fpga.add('fpga', part_name, 'var', f'{tool}_brams', [
            'spram_1024x64',
            'spram_2048x32',
            'spram_4096x16',
            'spram_8192x8',
            'spram_16384x4',
            'spram_32768x2',
            'spram_65536x1',
            'dpram_1024x32',
            'dpram_2048x16',
            'dpram_4096x8',
            'dpram_8192x4',
            'dpram_16384x2',
            'dpram_32768x1'])
        fpga.add('fpga', part_name, 'var', f'{tool}_dsps', [
            'efpga_adder',
            'efpga_adder_regi',
            'efpga_adder_rego',
            'efpga_adder_regio',
            'efpga_acc',
            'efpga_acc_regi',
            'efpga_mult',
            'efpga_mult_regi',
            'efpga_mult_rego',
            'efpga_mult_regio',
            'efpga_macc',
            'efpga_macc_regi',
            'efpga_macc_pipe',
            'efpga_macc_pipe_regi'])
