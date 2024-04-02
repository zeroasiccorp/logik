logik_demo Example eFPGA Architecture Model
===========================================

Logik ships with access to and support for an example eFPGA architecture model called logik_demo.  The logik_demo architecture does not target a specific process technology and so does not contain realistic timing information.  Instead, a unit delay model is used, where each delay parameter in the architecture is set to 1 ns.

The features of the logik_demo architecture are summarized in the table below:

+----------------------------------------------------------+--------+
| 4-input LUTs                                             | 6576   |
+----------------------------------------------------------+--------+
| Registers                                                | 6576   |
+----------------------------------------------------------+--------+
| GPIOs                                                    | 64     |
+----------------------------------------------------------+--------+
| `UMI Interfaces <https://github.com/zeroasiccorp/umi>`_  | 3      |
+----------------------------------------------------------+--------+
| 4KB Block RAMs                                           | 16     |
+----------------------------------------------------------+--------+
| Multiply-Add Engines (MAEs)                              | 16     |
+----------------------------------------------------------+--------+

logik_demo Logic Resources
--------------------------

The following sections briefly describe the logic resources of the logik_demo eFPGA at a high level.  Emphasis is placed on topics that are useful in studying the outputs of flow steps in Logik.

Lookup Tables and Registers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

logik_demo contains 4-input lookup tables (LUTs) for implementing general purpose logic.  During logic synthesis, digital logic is mapped to these LUTs.

Each LUT is paired with a D flip-flop to form a basic logic element (BLE).  BLE inputs and LUT inputs are wired together and thus equivalent.  Each flip flop can be configured with or without any of the following features:  asynchronous set, asynchronous reset, built-in enable bit.  Logic synthesis determines how many flip-flops are needed of each configuration type.  Placement and routing determine whether or not to pair LUT with its flip-flop.  Ifn the lut is paired, the BLE output receives the flip-flop output; otherwise, it receives the LUT output.  The BLE output interfaces to the FPGA's programmable interconnect. 

All LUTs are clustered into groups of eight to form configurable logic blocks (CLBs).  Each CLB shares 18 inputs amongst its eight LUTs.  The CLB contains local interconnect that allows a subset of the 18 CLB inputs, the 8 LUT outputs, and the 8 flip flop outputs to be selected as input to each BLE.

Multiply-Add Engine (MAE)
^^^^^^^^^^^^^^^^^^^^^^^^

The multiply-add engine (MAE) is a configurable arithmetic unit suitable for use in many digital signal processing (DSP) applications.  The key blocks are a multiplier and an adder, which can be used one at a time or together as a multiply-accumulate (MAC) unit.  An 18x18 multiplier receives data directly from the ebrick-fpga global interconnect or optionally from flip-flops to re-register data for improved throughput.  The output of the multiplier can be routed directly out of the MAE to global interconnect to realize a purely combinational multiplier circuit or routed through a bank of flip-flops.  In either case, this output can instead be routed through a 40-bit accumulator so that the MAE can be used as a MAC rather than a multiplier.  Both the multiplier and accumulator can be registered to create a pipelined MAC.  The accumulator can also be used by itself, in which case MAE inputs are routed directly to it. 

Each of these options maps to a specific MAE operational mode set by the configuration bitstream.  The MAE operational modes each map to a particular netlist macro name during synthesis.  The modes and their features are documented below:

+-------------+----------------------+----------------------------------+----------------+
| Function    | Synthesis Macro Name | Ports Registered                 | Latency        |
|             |                      |                                  | (clock cycles) |
+-------------+----------------------+----------------------------------+----------------+
| Multiply    | efpga_mult           | None                             | 0              | 
+-------------+----------------------+----------------------------------+----------------+
| Multiply    | efpga_mult_regi      | Inputs                           | 1              | 
+-------------+----------------------+----------------------------------+----------------+
| Multiply    | efpga_mult_rego      | Outputs                          | 1              | 
+-------------+----------------------+----------------------------------+----------------+
| Multiply    | efpga_mult_regio     | Inputs and Outputs               | 2              | 
+-------------+----------------------+----------------------------------+----------------+
| MAC         | efpga_macc           | Unpipelined, Inputs unregistered | 1              | 
+-------------+----------------------+----------------------------------+----------------+
| MAC         | efpga_macc_regi      | Unpipelined, Inputs registered   | 2              | 
+-------------+----------------------+----------------------------------+----------------+
| MAC         | efpga_macc_pipe      | Pipelined, Inputs unregistered   | 2              | 
+-------------+----------------------+----------------------------------+----------------+
| MAC         | efpga_macc_pipe_regi | Pipelined, inputs registered     | 3              | 
+-------------+----------------------+----------------------------------+----------------+
| Adder       | efpga_adder          | None                             | 0              | 
+-------------+----------------------+----------------------------------+----------------+
| Adder       | efpga_adder_regi     | Inputs                           | 1              | 
+-------------+----------------------+----------------------------------+----------------+
| Adder       | efpga_adder_rego     | Outputs                          | 1              | 
+-------------+----------------------+----------------------------------+----------------+
| Adder       | efpga_adder_regio    | Inputs and Outputs               | 2              | 
+-------------+----------------------+----------------------------------+----------------+
| Accumulator | efpga_macc_pipe      | Inputs unregistered              | 1              | 
+-------------+----------------------+----------------------------------+----------------+
| Accumulator | efpga_macc_pipe_regi | Inputs registered                | 2              |
+-------------+----------------------+----------------------------------+----------------+

Block RAMs (BRAMs)
^^^^^^^^^^^^^^^^^^

Each block RAM (BRAM) consists 8KB of single-port SRAM, organized as 2K 32-bit words.  The 8KB of SRAM can be used to emulate 4KB of simple dual-port SRAM with one write port, one read port, and one common clock.  It may also be used to emulate 1K 64-bit words when configured as single-port RAM.

Both single-port and dual-port operation support configurable bit widths and address depth.  Technology mapping during synthesis automatically maps RAMs of size > 8KB into multiple block RAM instances and selects one of the operating modes listed in the table below for the BRAM to operate in.  Each operating mode is delineated by a unique instance type in the synthesized netlist and specifies single-port or dual port, the effective word count, and the bits per word for the BRAM when in that mode.

+------------------+--------+-----------+----------------------+
| Port Type        | #Words | Bits/Word | Synthesis Macro Name |
+------------------+--------+-----------+----------------------+
| single-port      |  1024  | 64        | spram_1024x64        |
+------------------+--------+-----------+----------------------+
| single-port      |  2048  | 32        | spram_2048x32        |
+------------------+--------+-----------+----------------------+
| single-port      |  4096  | 16        | spram_4096x16        |
+------------------+--------+-----------+----------------------+
| single-port      |  8192  |  8        | spram_8192x8         |
+------------------+--------+-----------+----------------------+
| single-port      | 16384  |  4        | spram_16384x4        |
+------------------+--------+-----------+----------------------+
| single-port      | 32768  |  2        | spram_32768x2        |
+------------------+--------+-----------+----------------------+
| single-port      | 65536  |  1        | spram_65536x1        |
+------------------+--------+-----------+----------------------+
| simple dual-port |  1024  | 32        | dpram_1024x32        |
+------------------+--------+-----------+----------------------+
| simple dual-port |  2048  | 16        | dpram_2048x16        |
+------------------+--------+-----------+----------------------+
| simple dual-port |  4096  |  8        | dpram_4096x8         |
+------------------+--------+-----------+----------------------+
| simple dual-port |  8192  |  4        | dpram_8192x4         |
+------------------+--------+-----------+----------------------+
| simple dual-port | 16384  |  2        | dpram_16384x2        |
+------------------+--------+-----------+----------------------+
| simple dual-port | 32768  |  1        | dpram_32768x1        |
+------------------+--------+-----------+----------------------+

logik_demo eFPGA Port List
--------------------------

The table below enumerates logik_demo ports.  Each of these ports may be specified in a JSON pin constraints file (PCF) to specify where a user port should be mapped during place and route.

.. note:

   User ports must be mapped to logik_demo ports with matching directions

For more information on PCF, see :doc:`pin_constraints`

The logik_demo architecture has three types of I/O resources:

* Clocks -- three clock signals are provided.  All user clocks must map to one of three ports.  Designs with more than three clocks do not fit on this architectre.
* GPIOs -- 64 general purpose I/Os are provided.  Each GPIO is associated with one index of both the gpio_in port and the gpio_out port of the logik_demo top level.  For example, once a user port is assigned to gpio_in[0], gpio_out[0] may not be used for a user output.
* UMI interfaces -- logik_demo implements UMI interfaces as subsections of a wide I/O bus comprised of the umi_io_in and umi_io_out ports.  Like the GPIOs, each bit of the UMI interface bus is associated with one index of both the umi_io_in and umi_io_out busses.  For example, once a user port is assigned to umi_io_in[0], umi_io_out[0] may not be used for a user output.

+------------+-----------+-----------+------------------------------------------+
| Port Name  | Direction | Bit Range | Notes                                    |
+------------+-----------+-----------+------------------------------------------+
| clk        | input     | [2:0]     | All user clocks must map to these ports  |
+------------+-----------+-----------+------------------------------------------+
| gpio_in    | input     | [63:0]    | Pin locations are shared with gpio_out   |
+------------+-----------+-----------+------------------------------------------+
| gpio_out   | output    | [63:0]    | Pin locations are shared with gpio_in    |
+------------+-----------+-----------+------------------------------------------+
| umi_io_in  | input     | [3599:0]  | Pin locations are shared with umi_io_out |
+------------+-----------+-----------+------------------------------------------+
| umi_io_out | output    | [3599:0]  | Pin locations are shared with umi_io_in  |
+------------+-----------+-----------+------------------------------------------+

logik_demo UMI Port Mapping
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Included in the Logik flow support for logik_demo is a reference template auto-generating constraints that the UMI interfaces to top level ports.  In a complete eFPGA solution with UMI ports, that constraints generation template must correctly map eFPGA top level ports to specific locations elsewhere on chip that exchange UMI data between the eFPGA and other parts of the system.  The tables below show how the logik_demo umi_io_in and umi_io_out busses map to the three UMI ports supported by the architecture.

Device Request Port
+++++++++++++++++++

+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| UMI Signal          | UMI signal name    | UMI Port 1 Signal     | UMI Port 2 Signal     | UMI Port 3 Signal     |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Ready               | udev_req_ready     | umi_io_out[889]       | umi_io_out[2089]      | umi_io_out[3289]      |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Command             | udev_req_cmd       | umi_io_in[632:601]    | umi_io_in[1832:1801]  | umi_io_in[3032:3001]  |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Data                | udev_req_data      | umi_io_in[888:761]    | umi_io_in[2088:1961]  | umi_io_in[3288:3161]  |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Source Addresss     | udev_req_srcaddr   | umi_io_in[760:697]    | umi_io_in[1960:1897]  | umi_io_in[3160:3097]  |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Destination Address | udev_req_dstaddr   | umi_io_in[696:633]    | umi_io_in[1896:2133]  | umi_io_in[3096:3033]  |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Valid               | udev_req_valid     | umi_io_in[600]        | umi_io_in[1800]       | umi_io_in[3000]       |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+

Device Response Port
++++++++++++++++++++

+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| UMI Signal          | UMI signal name    | UMI Port 1 Signal     | UMI Port 2 Signal     | UMI Port 3 Signal     |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Ready               | uhost_req_ready    | umi_io_in[1189]       | umi_io_in[2389]       | umi_io_in[3589]       |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Command             | uhost_req_cmd      | umi_io_out[932:901]   | umi_io_out[2132:2101] | umi_io_out[3332:3301] |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Data                | uhost_req_data     | umi_io_out[1188:1061] | umi_io_out[2388:2261] | umi_io_out[3588:3461] |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Source Addresss     | uhost_req_srcaddr  | umi_io_out[1060:997]  | umi_io_out[2260:2197] | umi_io_out[3460:3397] |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Destination Address | uhost_req_dstaddr  | umi_io_out[996:933]   | umi_io_out[2196:2133] | umi_io_out[3396:3333] |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Valid               | uhost_req_valid    | umi_io_out[900]       | umi_io_out[2100]      | umi_io_out[3300]      |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+

Host Request Port
+++++++++++++++++++

+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| UMI Signal          | UMI signal name    | UMI Port 1 Signal     | UMI Port 2 Signal     | UMI Port 3 Signal     |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Ready               | uhost_req_ready    | umi_io_in[289]        | umi_io_in[1489]       | umi_io_in[2689]       |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Command             | uhost_req_cmd      | umi_io_out[32:1]      | umi_io_out[1232:1201] | umi_io_out[2432:2401] |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Data                | uhost_req_data     | umi_io_out[288:161]   | umi_io_out[1488:1361] | umi_io_out[2688:2561] |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Source Addresss     | uhost_req_srcaddr  | umi_io_out[160:97]    | umi_io_out[1360:1297] | umi_io_out[2560:2497] |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Destination Address | uhost_req_dstaddr  | umi_io_out[96:33]     | umi_io_out[1296:1233] | umi_io_out[2496:2433] |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Valid               | uhost_req_valid    | umi_io_out[0]         | umi_io_out[1200]      | umi_io_out[2400]      |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+

Host Response Port
++++++++++++++++++++

+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| UMI Signal          | UMI signal name    | UMI Port 1 Signal     | UMI Port 2 Signal     | UMI Port 3 Signal     |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Ready               | uhost_resp_ready   | umi_io_out[589]       | umi_io_out[1789]      | umi_io_out[2989]      |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Command             | uhost_resp_cmd     | umi_io_in[332:301]    | umi_io_in[1532:1501]  | umi_io_in[2732:2701]  |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Data                | uhost_resp_data    | umi_io_in[588:461]    | umi_io_in[1788:1661]  | umi_io_in[2988:2861]  |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Source Addresss     | uhost_resp_srcaddr | umi_io_in[460:397]    | umi_io_in[1660:1597]  | umi_io_in[2860:2797]  |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Destination Address | uhost_resp_dstaddr | umi_io_in[396:333]    | umi_io_in[1596:1533]  | umi_io_in[2796:2733]  |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+
| Valid               | uhost_resp_valid   | umi_io_in[300]        | umi_io_in[1500]       | umi_io_in[2700]       |
+---------------------+--------------------+-----------------------+-----------------------+-----------------------+


Notes on logik_demo Model for Developers
----------------------------------------

.. note::

   The developer model for adding new FPGAs to Logik is a work in progress.  Collaboration is strongly recommended to assist in the bringup of a new FPGA architecture in Logik.

Developers interested in studying the logik_demo model as a reference model for adding a new FPGA to Logik may wish to understand the model in more detail.  Below is a summary of the required FPGA model files that developers must provide to support an FPGA in Logik.

* A VPR architecture XML file is required.  For bitstream generation support, it must contain FASM feature metadata for all required features.
* A VPR routing resource graph XML file is also required.  While VPR supports flows that do not use this file, routing resource graph XML metadata is required for bitstream generation with genfasm.
* A bitstream map file is required for Logik bitstream finishing.  The bitstream map file is a JSON document that embeds the location of each FASM feature within a four-dimensional address space defined by the architecture's bitstream loading sequence.
* A constraints map file is required for support of JSON pin constraints (PCF) to VPR's native XML placement constraints format.
* For support of technology mapping by Yosys of FPGA hard macros, Yosys-compatible Verilog models are required.  These must be co-designed with the VPR architecture XML to ensure compatibility across all steps of the flow.

In addition to these model files, a part driver must be added to Logik for any group of related FPGAs or eFPGAs (referred to as FPGA/eFPGA families).  The part driver may share information between multiple FPGAs in a family, or define data only for a single FPGA/eFPGA.  The part driver is a Python file created as a module within the Logik Python package hierarchy.  This means that the part driver must be formally integrated into a Logik release.

Within the logik_demo part driver provided with Logik, these files are specified and registered as Silicon Compiler packages.  Silicon Compiler is then able to acquire the files for use in the Logik flow.  Additional FPGA/eFPGA design-specific data required by CAD tools, such as the input counts of LUTs in the FPGA or the number of routing resources, must also be specified.  Consult the logik_demo example for reference on these details.
