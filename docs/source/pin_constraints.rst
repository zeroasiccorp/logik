Preparing Pin Constraints
=========================

VPR Placement Constraints
-------------------------

VPR natively supports pin constraint specification as a subset of its generic placement constraint settings.  VPR placement constraints are specified in XML format.  Complete documentation of this format is provided as part of `VPR documentation`_.

To make use of these constraints it is necessary to have detailed information about the structure of the FPGA that is being targeted.  FPGA resources are mapped in VPR to a grid laid out on an (X,Y) coordinate system.

For eebrick-fpga chiplets, knowledge of this coordinate system is not necessary.  Instead, a port-to-port mapping between user ports and ebrick-fpga embedded FPGA ports can be specified in JSON format.  This format is described below.


JSON Pin Constraints
--------------------
For ebrick-fpga chiplets, specifying pin constraints in JSON format is supported so that users can specify a mapping between ports in their top-level RTL and ports in the standardized ebrick_core port list.

The JSON pin constraint file is organized as a dictionary of JSON objects where keys in the dictionary are user port names and values are two-element dictionaries containing the port direction and the ebrick_core port name to which that user port should be mapped.  The port direction is specified with the "direction" key and the the ebrick_core port name is specified with the "pin" key.  This syntax is shown in the example below:

Example Pin Constraint Syntax
`````````````````````````````

```
  "resetn": {
    "direction": "input",
    "pin": "gpio_in_left[1]"
  },
```
