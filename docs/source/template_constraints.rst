Automating Pin Constraint Generation for UMI Ports
==================================================

A full UMI interface with both device and host request and response ports requires 1180 signals.  To automate the pin constraint generation for UMI ports, two strategies are possible:

* Users may make use of UMI pin constraint templates provided with this software 
* Users may develop their own automation scripts for generating UMI port constraints

Importing UMI Pin Constraints from a Template
----------------------------------------------------

eFPGA devices with UMI interfaces require an exact set of pin constraints that is used to connect user-defined UMI ports to the corresponding UMI port signals internal to the FPGA core.  The required pin constraints are the same for all users, so a template for these constraints is provided for import into users' Silicon Compiler run scripts.

To make use of the pin constraints template, users must do the following:

* Integrate the constraints template into Python code for generating pin constraints.
* Follow the UMI port naming convention described below in their RTL

Constraints Template Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

eFPGA UMI pin constraint templates are implemented as Python functions.  For each UMI-enabled eFPGA device, there is a corresponding Python module called umi_pin_constraints.py provided as part of the templates submodule of this software.  Each module contains a function called

::

   generate_umi_pin_constraints

This can be imported into a user-defined pin constraints generator using
   
::

   import logik.templates.<eFPGA part name>.umi_pin_constraints as <eFPGA part name>

The function takes a standard set of parameters that can be used to control constraints generation behavior.  The API is as follows:


::

   generate_umi_pin_constraints(fpga_ports_per_umi=300,
                                umi_cmd_width=32,
                                umi_data_width=128,
                                umi_addr_width=64,
                                umi_ports_used=[1, 2, 3],
                                port_types=["uhost_req",
                                            "uhost_resp",
                                            "udev_req",
                                            "udev_resp"],
                                umi_port_num_offset=1,
                                index_control_bits=True)

The meaning of these parameters is described in the table below

+---------------------+-----------------------------------------------------------------------------------------------------------+
| fpga_ports_per_umi  | this parameter is used to define how many fpga pins are internally allocated for each UMI interface port. |
|                     | Except in rare circumstances, the default value should be used.                                           |
+---------------------+-----------------------------------------------------------------------------------------------------------+
| umi_cmd_width       | sets the number of bits in the UMI command bus                                                            |
+---------------------+-----------------------------------------------------------------------------------------------------------+
| umi_data_width      | sets the number of bits in the UMI data bus                                                               |
+---------------------+-----------------------------------------------------------------------------------------------------------+
| umi_addr_width      | sets the number of bits in the UMI source and destination address busses                                  |
+---------------------+-----------------------------------------------------------------------------------------------------------+
| umi_ports_used      | Each UMI port in is numbered.  UMI port 0 is reserved for bitstream loading.                              |
|                     | UMI ports 1, 2, and 3 are user-accessible.  This parameter allows specification of which                  |
|                     | of the UMI ports are used in user RTL code.  Changing this value to enumerate only ports                  |
|                     | that are used prevents unused constraints from being generated.                                           |
+---------------------+-----------------------------------------------------------------------------------------------------------+
| umi_port_num_offset | Defines an offset between FPGA internal bus indices and UMI port numbers.                                 |
|                     | Except in rare circumstances, the default value should be used.                                           |
+---------------------+-----------------------------------------------------------------------------------------------------------+
| index_control_bits  | Defines whether constraints are generated such that UMI port ready and valid signals are                  |
|                     | specified with bus indices.  In general, user RTL code with multiple UMI ports defined                    |
|                     | should set this to True, while user RTL code using a single UMI port should set this to                   |
|                     | False                                                                                                     |
+---------------------+-----------------------------------------------------------------------------------------------------------+
  
Pin Constraint Template UMI Port Naming Conventions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following tables show what signal names must be used in user RTL to name UMI interface signals for compatibility with eFPGA UMI pin constraint templates.

All signals with names ending in "ready" or "valid" may be specified as scalars or as multi-bit busses.  When specified as scalars, calls to the generate_umi_pin_constraints constraint template generator functions must set the index_control_bits parameter to False.

Device Request Port
+++++++++++++++++++

+---------------------+--------------------+
| Ready               | udev_req_ready     |
+---------------------+--------------------+
| Command             | udev_req_cmd       |
+---------------------+--------------------+
| Data                | udev_req_data      |
+---------------------+--------------------+
| Source Addresss     | udev_req_srcaddr   |
+---------------------+--------------------+
| Destination Address | udev_req_dstaddr   |
+---------------------+--------------------+
| Valid               | udev_req_valid     |
+---------------------+--------------------+

Device Response Port
++++++++++++++++++++

+---------------------+--------------------+
| Ready               | udev_resp_ready    |
+---------------------+--------------------+
| Command             | udev_resp_cmd      |
+---------------------+--------------------+
| Data                | udev_resp_data     |
+---------------------+--------------------+
| Source Addresss     | udev_resp_srcaddr  |
+---------------------+--------------------+
| Destination Address | udev_resp_dstaddr  |
+---------------------+--------------------+
| Valid               | udev_resp_valid    |
+---------------------+--------------------+


Host Request Port
+++++++++++++++++++

+---------------------+--------------------+
| Ready               | uhost_req_ready    |
+---------------------+--------------------+
| Command             | uhost_req_cmd      |
+---------------------+--------------------+
| Data                | uhost_req_data     |
+---------------------+--------------------+
| Source Addresss     | uhost_req_srcaddr  |
+---------------------+--------------------+
| Destination Address | uhost_req_dstaddr  |
+---------------------+--------------------+
| Valid               | uhost_req_valid    |
+---------------------+--------------------+

Host Response Port
++++++++++++++++++++

+---------------------+--------------------+
| Ready               | uhost_resp_ready   |
+---------------------+--------------------+
| Command             | uhost_resp_cmd     |
+---------------------+--------------------+
| Data                | uhost_resp_data    |
+---------------------+--------------------+
| Source Addresss     | uhost_resp_srcaddr |
+---------------------+--------------------+
| Destination Address | uhost_resp_dstaddr |
+---------------------+--------------------+
| Valid               | uhost_resp_valid   |
+---------------------+--------------------+

Developing Custom Automation Scripts for Generating UMI Pin Constraints
-----------------------------------------------------------------------

It is also possible to generate a custom automation script for generating UMI port pin constraints.  While always possible, it is only required if the UMI port naming convention documented above cannot be followed in user RTL.

Any automation technique that produces a valid JSON pin constraints file may be used.  However, only a Python-based approach can be inlined with a Silicon Compiler run script.
