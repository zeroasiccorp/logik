Preparing Timing Constraints for VPR
====================================

.. note::

   The demo architecture provided with this distrbution implements a unit delay model.  Provided examples demonstrate the Logik without an SDC file.  Examples that include SDC files are planned for a future release.

VPR is the place and route engine used in the Logik RTL to bitstream flow.  To support VPR's timing-driven place and route flow, timing constraints are provided in a Synopsys Design Constraint (SDC) file.

The minimum requirement is to specify a target clock frequency using the `create_clock` constraint:

::
   
   create_clock -period <float> <name of clock port>

For specifics on VPR's supported timing constraints, please consult the `VPR SDC Commmand support page <https://docs.verilogtorouting.org/en/latest/vpr/sdc_commands/>`_
