# ebrick-fpga-cad
RTL-to-bitstream and other CAD support for ebrick-fpga

## Repository Setup
To prepare this repository for use, it is necessary to do the following:

* Install required software tools.  Currently these are [Yosys](https://yosyshq.readthedocs.io/en/latest/tools.html#yosys), [VPR](https://docs.verilogtorouting.org), and [Silicon Compiler](https://docs.siliconcompiler.com).  There are two ways to do this
    1. Obtain via Silicon Compiler installation
    2. Build from source yourself: 
        * [Yosys Github repository](https://github.com/YosysHQ) [Yosys build instructions](https://github.com/YosysHQ/yosys?tab=readme-ov-file#installation)
        * [VPR Github repository](https://github.com/verilog-to-routing/vtr-verilog-to-routing/tree/master)[VPR build instructions](https://github.com/verilog-to-routing/vtr-verilog-to-routing/blob/master/BUILDING.md)
* Clone this repository:  `git clone https://github.com/zeroasiccorp/ebrick-fpga-cad`
* Create a Python virtual environment, e.g. `python3 -m venv venv; source venv/bin/activate`
* Install Python packages within your virtual environment; `pip install --upgrade pip; pip install -r requirements.txt`
* Set up authentication to the Silicon Compiler package registry.

> [!NOTE]
> Currently authentication is validated for Zero ASIC employees only; to set up, set the GIT_TOKEN environment variable in your shell equal to the value of your Github personal access token.

* Append the root directory where you have cloned this repository to your PYTHONPATH; e.g. `export PYTHONPATH=${PYTHONPATH}:${PWD}` if your present working directory is the root directory of your repo clone.

## Running Examples

There are two example circuits provided to demonstrate the Silicon Compiler RTL-to-bitstream flow for ebrick-fpga:  an adder and a FIR filter.  The instructions below are for the FIR filter; running the adder is the same except for the directory and file names that are used.

Within the python virtual environment set up as described above and starting from your ebrick-fpga-cad repo clone root directory, run the following:

* `cd examples/fir_filter/sc`
* `python3 fir_filter.py`


