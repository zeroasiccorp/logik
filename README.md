# ebrick-fpga-cad
This repository contains RTL-to-bitstream and other CAD support for ebrick-fpga.

This README documents how to set up and make use of the software contained in this repository, and how to run example scripts that showcase software features.

## Prerequisites

* Ubuntu 20.04
* Python 3.8 or higher
* git

Github CLI is not required, but recommended.

## Install Required Software

Currently the required tools are [Yosys](https://yosyshq.readthedocs.io/en/latest/tools.html#yosys), [VPR](https://docs.verilogtorouting.org), and [Silicon Compiler](https://docs.siliconcompiler.com).  There are two ways to do this
    1. Obtain via Silicon Compiler installation
    2. Build from source yourself.  This requires checking out the qualified versions of the source repositories, which are documented in instructions below

### Silicon Compiler Installation
Silicon Compiler is installed as part of the python package requirements for this repository (see below)

### Yosys Installation
* Clone the [Yosys Github repository](https://github.com/YosysHQ)
* Check out the current qualified version:  `git checkout yosys-0.36`
* Follow the [Yosys build instructions](https://github.com/YosysHQ/yosys?tab=readme-ov-file#installation)
* Add the path to the yosys executable to your PATH environment variable

### VPR Installation
* Clone the [VPR Github repository](https://github.com/verilog-to-routing/vtr-verilog-to-routing/tree/master)
* Check out the current qualified version:  `git checkout c4156f225c7a292c5768444631ca053ea7473428`
* Follow the [VPR build instructions](https://github.com/verilog-to-routing/vtr-verilog-to-routing/blob/master/BUILDING.md)
* Add the paths to the vpr and genfasm executables to your PATH environment variable

## Repository Setup
To prepare this repository for use, it is necessary to do the following:

* Clone this repository:  `git clone https://github.com/zeroasiccorp/ebrick-fpga-cad`
* Create a Python virtual environment, e.g. `python3 -m venv venv; source venv/bin/activate`
* Install Python packages within your virtual environment; `pip install --upgrade pip; pip install -e .`
* Set up authentication to the Silicon Compiler package registry.

> [!NOTE]
> Currently authentication is validated for Zero ASIC employees only; to set up, set the GIT_TOKEN environment variable in your shell equal to the value of your Github personal access token.

* Append the root directory where you have cloned this repository to your PYTHONPATH; e.g. `export PYTHONPATH=${PYTHONPATH}:${PWD}` if your present working directory is the root directory of your repo clone.

## Running Examples

There are three example circuits provided to demonstrate the Silicon Compiler RTL-to-bitstream flow for ebrick-fpga: an adder, an FIR filter, and a "hello world" circuit for use with our web-based emulation tool.

### FIR filter and adder

The instructions below are for the FIR filter; running the adder is the same except for the directory and file names that are used.

Within the Python virtual environment set up as described above and starting from your ebrick-fpga-cad repo clone root directory, run the following:

```console
cd examples/umi_fir_filter
```

```console
python3 umi_fir_filter.py
```

### Hello world circuit

This example shows how to run a generated bitstream with web-based emulation.  The RTL implemented on the FPGA sends a hello world message as a sequence of characters to a special address that causes the characters to be printed out when run in an emulation environment.

As with the previous examples, first build a bitstream:

```console
cd examples/umi_hello
```

```console
python3 umi_hello.py
```

Then:
1. In a web browser, go to [https://preview.zeroasic.com/emulation](https://preview.zeroasic.com/emulation).  (TODO: replace with non-preview URL)
2. Log in if necessary (menu in the upper right corner)
3. Under "Select a Demo" on the left side of the window, click "FPGA"
4. Click "Suggest Layout"
5. In the middle of the page, click "Emulate"
6. Wait for the Linux Terminal to display a prompt.  (may take a few minutes)
7. Click "Upload File" and select `ebrick-fpga-cad/examples/umi_hello/build/umi_hello/job0/bitstream/0/outputs/umi_hello.dat` (this is the bitstream you just built)
8. Wait for the status bar to indicate that the file upload was successful.
9. In the Linux Terminal shell, type `init-fpga.sh` (this script is in the `PATH`, so no need to `cd` anywhere)
10. Scroll down to the Output Terminal.  You should see the text `Hello World!` appear in a few seconds, if it's not already there.

Suggested next step: try modifying the hello world string in `ebrick-fpga-cad/examples/umi_hello/rtl/umi_hello.v`, rebuild the bitstream, and go through steps 7-10 (i.e., from uploading the bitstream onwards) to run the new bitstream. 
