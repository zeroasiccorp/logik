# ebrick-fpga-cad
This repository contains RTL-to-bitstream and other CAD support for ebrick-fpga.

HDL simulation support is not explicitly provided within this repository.  However, [Silicon Compiler](https://siliconcompiler.com) supports HDL simulation flows using open source simulators.  Consult Silicon Compiler documentation for details.

The RTL-to-bitstream flow is implemented as a custom [Silicon Compiler](https://siliconcompiler.com) flow graph:

![image info](images/fpga_flow.png)

This README documents how to set up and make use of the software contained in this repository, and how to run the flow on an example design to test your setup.  

## System Software Requirements

* Ubuntu 20.04
* Python 3.8 or higher
* git

## Installing Required EDA Software

This flow makes use of several open-source electronic design automation (EDA) tools.  Currently the minimum required EDA tools are:

* [Surelog](https://github.com/chipsalliance/Surelog)
* [Yosys](https://yosyshq.readthedocs.io/en/latest/tools.html#yosys)
* [VPR](https://docs.verilogtorouting.org),
* [Silicon Compiler](https://docs.siliconcompiler.com).

For VHDL support, [GHDL](https://ghdl.github.io/ghdl/) is also required.

For SystemVerilog support, [sv2v](https://github.com/zachjs/sv2v?tab=readme-ov-file#sv2v-systemverilog-to-verilog) is also required.

To integrate this software with a complete FPGA development environment or to run HDL simulations on provided examples, simulation tools are also needed.  The following open source options are available:

* [GTKWave](https://gtkwave.sourceforge.net/)
* [IcarusVerilog](http://iverilog.icarus.com/)
* [Verilator](https://verilator.org/guide/latest/)

There are two options for setting up these tools:  running within a docker container and installing required software locally.

### Running Within Docker

First, install Docker if you haven't already.  Here are the instructions for various platforms:
* [Linux Docker installation](https://docs.docker.com/desktop/install/linux-install/)
* [macOS Docker installation](https://docs.docker.com/desktop/install/mac-install/)
* [Windows Docker installation](https://docs.docker.com/desktop/install/windows-install/)

Once Docker is installed, launch the Docker Desktop application.

Then launch a terminal:
* Ubuntu: `Ctrl`-`Alt`-`T` or run the Terminal application from the Dash
* macOS: `Cmd-Space` to open Spotlight, then type `Terminal` and press `Enter`
* Windows: Open `Windows PowerShell` from the Start menu.

```console
docker run -it -v "${PWD}/sc_work:/sc_work" ghcr.io/siliconcompiler/sc_runner:latest
```

### Installing Required Software Manually

If you do not have docker installed, or you wish to install tools directly on your system, [Silicon Compiler's install scripts](https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools) may also be consulted.  Please bear in mind these are furnished for reference only; your system may impose additional or alternative requirements.  

The definitive authority for each tool is its own documentation; links are provided above.

## Repository Setup
To prepare this repository for use, it is necessary to do the following.  If you run within docker, these commands should be run inside your docker container:

* Clone this repository:  `git clone https://github.com/zeroasiccorp/ebrick-fpga-cad`
* Create a Python virtual environment, e.g. `python3 -m venv venv; source venv/bin/activate`
* Install Python packages within your virtual environment: `pip install --upgrade pip; pip install .`
* (required only for running examples) Install additional packages for running examples: `pip install .[examples]`
* Build documentation:  `pip install .[docs]; cd docs; make html`

## Testing Setup:  RTL-to-Bitstream for an 8-bit Adder

To test your setup, run the following to try the flow on a trivial circuit (8-bit adder):

```console
cd examples/adder
python3 adder.py
```

## Running a Bitstream with Cloud Emulation

To test out a bitstream with our web-based emulation tool, try running the hello world example in [examples/umi_hello](examples/umi_hello).  In that example, RTL implemented on ebrick-fpga sends a hello world message as a sequence of characters to an address that causes the characters to be printed out when run in an emulation environment.

As with the adder example, first build a bitstream:

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
7. Copy-paste the following command into the Linux Terminal and run it to fix the `init-fpga.sh` script (TODO: remove the need for this)
```console
head -n 14 /usr/bin/init-fpga.sh > temp && echo "sudo gridrw \$FPGA_LOC chiplet 0x4000000000 l 0
sudo gridrw \$FPGA_LOC chiplet 0x1000000000 l 0
sudo gridrw \$FPGA_LOC chiplet 0x1000000000 l 1
sudo gridrw \$FPGA_LOC chiplet 0x4000000000 l 1" >> temp && sudo mv temp /usr/bin/init-fpga.sh && sudo chmod +x /usr/bin/init-fpga.sh
```
8. Click "Upload File" and select `ebrick-fpga-cad/examples/umi_hello/build/umi_hello/job0/bitstream/0/outputs/umi_hello.dat` (this is the bitstream you just built)
9. Wait for the status bar to indicate that the file upload was successful.  (should take 5-10 seconds)
10. In the Linux Terminal shell, type `init-fpga.sh` (this script is in the `PATH`, so no need to `cd` anywhere)
11. Scroll down to the Output Terminal.  You should see the text `Hello World!` appear in a few seconds, if it's not already there.

Suggested next step: try modifying the hello world string in `ebrick-fpga-cad/examples/umi_hello/rtl/umi_hello.v`, rebuild the bitstream, and go through steps 8-11 (i.e., from uploading the bitstream onwards) to run the new bitstream. 

## Additional Examples and Documentation

To run additional examples and learn more about the flow, please consult the user guide built in the repository setup step; this can be accessed by opening

```console
firefox ./docs/build/html/index.html
```
