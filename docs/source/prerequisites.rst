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

+------------------------------+------------------------------------------------------------------------------------------------+
| Silicon Compiler             | `SC Documentation <https://docs.siliconcompiler.com>`_                                         |
+------------------------------+------------------------------------------------------------------------------------------------+
| Surelog                      | `Surelog Documentation <https://github.com/chipsalliance/Surelog?tab=readme-ov-file#surelog>`_ |
+------------------------------+------------------------------------------------------------------------------------------------+
| Verilog-to-Routing (VPR)     | `VPR Documentation <https://docs.verilogtorouting.org/en/latest/>`_                            |
+------------------------------+------------------------------------------------------------------------------------------------+
| Yosys                        | `Yosys Documentation <https://yosyshq.readthedocs.io/en/latest/>`_                             |
+------------------------------+------------------------------------------------------------------------------------------------+

For VHDL support, `GHDL <https://ghdl.github.io/ghdl/>`_ is also required.

For SystemVerilog support, `sv2v <https://github.com/zachjs/sv2v?tab=readme-ov-file#sv2v-systemverilog-to-verilog>`_ is also required.


Optional EDA Software Tools
---------------------------

While not required to run the RTL-to-bitstream flow, HDL simulation support is required to run HDL simulations on provided examples.

Either of the following open-source simulators may be used for HDL simulation:

+------------------------------+------------------------------------------------------------------------+
| Icarus Verilog               | `Icarus Documentation <http://iverilog.icarus.com/>`_                  |
+------------------------------+------------------------------------------------------------------------+
| Verilator                    | `Verilator Documentation <https://verilator.org/guide/latest/>`_       |
+------------------------------+------------------------------------------------------------------------+

For waveform viewing, GTKWave is an available open source viewer:

+------------------------------+------------------------------------------------------------------------+
| GTKWave                      | `Gtkwave Documentation <https://gtkwave.sourceforge.net/>`_            |
+------------------------------+------------------------------------------------------------------------+
