from siliconcompiler.package import register_private_github_data_source


fpga_version = 'v0.1.22'


def register_package(fpga, package_name, artifact):
    register_private_github_data_source(
        fpga,
        package_name,
        repository='zeroasiccorp/logik',
        release=fpga_version,
        artifact=artifact)


def set_fpga_resources(fpga):
    part_name = fpga.design

    fpga.add('fpga', part_name, 'resources', 'registers', [
        'dff',
        'dffr',
        'dffs',
        'dffe',
        'dffer',
        'dffes',
        'dffrs',
        'dffers'])
    fpga.add('fpga', part_name, 'resources', 'brams', [
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
    fpga.add('fpga', part_name, 'resources', 'dsps', [
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
