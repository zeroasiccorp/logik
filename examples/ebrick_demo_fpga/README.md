# ebrick-demo RTL-to-bitstream Example

This example demonstrates how Silicon Compiler's package manager can be used to import design data from another project and use it in the Logik flow.

In this case, the imported design data is the ebrick-demo design.  For more information on ebrick-demo, see its [Github repository](https://github.com/zeroasiccorp/ebrick-demo).  To adapt ebrick-demo for use in an FPGA design instead of as an ASIC, a thin Verilog wrapper is provided to adapt the ebrick-demo pin list to one that is compatible with the logik_demo eFPGA architecture.

To run this example, run

```
python3 ebrick_demo_fpga.py
```
