# UMI FIR Filter Peripheral

This example demonstrates an accelerator with a UMI interface.  In this case, the accelerator is a simple FIR filter.  By working with this example, you can see how Logik can make use of integrated pin constraint templates to reduce effort in preparing pin constraints.

To run this example, install Logik if you haven't already:

```console
python -m pip install --upgrade logik
```

Then install Logik examples' package dependencies:

```console
pip install -r examples/requirements.txt
```

Then in this directory run

```
python3 umi_fir_filter.py
```

A script called pin_constraints.py is contained within this example.  This script is used to auto-generate pin constraints.  Output of this script specific to logik_demo eFPGA has been included in the repository.  The generator uses a constraints generation template function provided for the logik_demo eFPGA to automatically map UMI interface signals with pre-set names to their corresponding top level ports on the logik_demo eFPGA.  The template is imported as a Python module.  For additional information on how these constraints are generated, see the [Logik documentation's discussion of templated pin constraints](https://logik.readthedocs.io/en/latest/template_constraints.html).

