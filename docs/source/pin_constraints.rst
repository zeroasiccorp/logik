Preparing Pin Constraints and Placement Constraints
===================================================

Execution of the placement and routing steps with VPR do not require specifying constraints for the location of top-level ports in the user RTL design.  When no constraints are specified, VPR will automatically choose locations for ports using its placement algorithm.

In some architectures (including the architecture supplied for the examples in this distribution), pin constraints are required in order to specify which of a subset of FPGA pins may be used as clock signals.  More practically, constraints are typically required on all ports so that signals are routed to the correct physical locations for interaction with other components.  Constraints may also be specified for the physical location of logic blocks.

The methods of supplying these constraints are described below.

VPR Placement Constraints
-------------------------

VPR natively supports pin constraint specification as a subset of its generic placement constraint settings.  VPR placement constraints are specified in XML format.  Complete documentation of this format is provided as part of `VPR documentation <https://docs.verilogtorouting.org/en/latest/vpr/placement_constraints/>`_.

To make use of these constraints it is necessary to have detailed information about the structure of the FPGA that is being targeted.  FPGA resources are mapped in VPR to a grid laid out on an (X,Y) coordinate system.

Use of this format is required in order to constrain the placement of logic blocks.  However, typically specifying placement constraints for logic blocks is not necessary in this RTL-to-bitstream flow.

If only pin constraints need to be specified, knowledge of this coordinate system is not necessary.  Instead, a port-to-port mapping between user ports and eFPGA ports/FPGA pins can be specified in JSON format.  This format is described below.


JSON Pin Constraints (PCF)
--------------------------
Specifying pin constraints in JSON format is supported so that users can specify a mapping between ports in their top-level RTL and port or pin names defined in the FPGA architecture.  The required structure of the JSON file is referred to within Silicon Compiler as PCF format to distinguish it from other JSON files, and the .pcf file extension is used as an indicator that a file is of this type.

The PCF file is organized as a dictionary of JSON objects where keys in the dictionary are user port names and values are two-element dictionaries containing the port direction and the FPGA top level port name to which that user port should be mapped.  The port direction is specified with the "direction" key and the the FPGA top level port name is specified with the "pin" key.  This syntax is shown in the example below:

Example Pin Constraint Syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::
   
  "resetn": {
    "direction": "input",
    "pin": "gpio_in[1]"
  },

