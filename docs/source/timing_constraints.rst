Preparing Timing Constraints for VPR
====================================

VPR is the place and route engine used in Zero ASIC FPGA chiplet and eFPGA chiplet RTL-to-bitstream flows.  To support VPR's timing-driven place and route flow, timing constraints are provided in a Synopsys Design Constraint (SDC) file.

The minimum requirement is to specify a target clock frequency using the `create_clock` constraint:

```
create_clock <>
```

For specifics on VPR's supported timing constraints, please consult the `VPR SDC Commmand support page<https://docs.verilogtorouting.org/en/latest/vpr/sdc_commands/>`_