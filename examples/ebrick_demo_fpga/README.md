# ebrick-demo RTL-to-bitstream Example

This example demonstrates how Silicon Compiler's package manager can be used to import design data from another project and use it in the Logik flow.

In this case, the imported design data is the ebrick-demo design.  For more information on ebrick-demo, see its [Github repository](https://github.com/zeroasiccorp/ebrick-demo).  To adapt ebrick-demo for use in an FPGA design instead of as an ASIC, a thin Verilog wrapper is provided to adapt the ebrick-demo pin list to one that is compatible with the logik_demo eFPGA architecture.

To run this example, install Logik if you haven't already:

```console
python -m pip install --upgrade logik
```

Then in this directory install this example's package dependencies:

```console
pip install -r requirements.txt
```

Then run

```
python3 ebrick_demo_fpga.py
```

This script contains a section specifically for importing the ebrick-demo design using Silicon Compiler's package registry.  For additional information, see the [Logik documentation's discussion of Silicon Compiler run script preparation](https://logik.readthedocs.io/en/latest/sc_preparation.html) and [Silicon Compiler's documentation of registering package sources](https://docs.siliconcompiler.com/en/stable/reference_manual/core_api.html#siliconcompiler.Chip.register_package_source).
