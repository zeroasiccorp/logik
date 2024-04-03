System Software Requirements
============================

Supported Operating Systems
---------------------------

The following operating systems are supported without the requirement of running within a docker container:

* Ubuntu 20.04

Additional OS support is provided by running within a docker container.

General Purpose Software Requirements
-------------------------------------

The following general purpose software must be installed on your system to use this flow:

* Python 3.8 or higher
* git

Required EDA Software Tools
---------------------------

* Silicon Compiler
* Surelog
* Yosys
* VPR

For VHDL support, GHDL is also required

For SystemVerilog support, sv2v is also required.

For links to all EDA software Github repositories and documentation pages, please consult the :doc:`external_links`.

Optional EDA Software Tools
---------------------------

While not required to run the RTL-to-bitstream flow, HDL simulation support is required to run HDL simulations on provided examples.

Either of the following open-source simulators may be used for HDL simulation:

* Icarus Verilog
* Verilator
  
For waveform viewing, GTKWave is an available open source viewer:

* GTKWave
  
For links to all EDA software Github repositories and documentation pages, please consult the :doc:`external_links`.

