Design Preparation
==================

Prior to running the RTL-to-bitstream flow, design data must be aggregated and organized so that it can be found during flow execution.  The effort to do this is minimal and outlined below.

Create a Working Directory
--------------------------

Because the flow is command-line driven, organization of files is performed at the command line rather than through an integrated development environment (IDE) project-based infrastructure.  It is strongly recommended that users create a dedicated directory tree in which to store HDL files, constraint files, and their Silicon Compiler run script.  It is also recommended (though not required) to execute the RTL-to-bitstream flow from the directory containing the Silicon Compiler run script.

Aggregate Input Files
---------------------

The following file types should be aggregated

* HDL files
* Timing Constraints
* Pin Constraints

With these in place, a Silicon Compiler run script will have all required input files for execution.

