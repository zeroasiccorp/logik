# UMI FIR Filter Peripheral

This example demonstrates an accelerator with a UMI interface.  In this case, the accelerator is a simple FIR filter.  By working with this example, you can see how Logik can make use of integrated pin constraint templates to reduce effort in preparing pin constraints.

The file

```
constraints/pin_constraints.py
```

contained within this example can be used to auto-generate pin constraints.  For use with the logik_demo eFPGA, the output of this script has been included with Logik.  The generator uses a constraints generation template function provided for the logik_demo eFPGA to automatically map UMI interface signals with pre-set names to their corresponding top level ports on the logik_demo eFPGA.  The template is imported as a Python module.  For additional information on how these constraints are generated, see [Logik Documentation]()

To run this example, run

```
python3 umi_fir_filter.py
```
