# UMI Fir Filter Simulation Testbench

This directory contains the infrastructure to set up and run a switchboard-based simulation of the FIR filter with data streaming in and out of the filter block using UMI protocol.

To run the simulation, cd into this directory and run the following

```
make
python3 umi_fir_filter_test.py
```

This will produce a waveform database in logs/umi_fir_filter.vcd that can be viewed to analyze the UMI traffic going in and out of the filter.
