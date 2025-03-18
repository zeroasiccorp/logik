![Logik](https://raw.githubusercontent.com/siliconcompiler/logik/main/images/logik_logo_with_text.png)

[![Regression](https://github.com/siliconcompiler/logik/actions/workflows/regression.yml/badge.svg)](https://github.com/siliconcompiler/logik/actions/workflows/regression.yml)
[![Lint](https://github.com/siliconcompiler/logik/actions/workflows/lint.yml/badge.svg)](https://github.com/siliconcompiler/logik/actions/workflows/lint.yml)

-----------------------------------------------------------------------------------

Logik is an open source FPGA tool chain with support for high level language parsing, synthesis, placement, routing, bit-stream generation, and analysis. Users enter design sources, constraints, and compile options through a simple [SiliconCompiler](https://github.com/siliconcompiler/siliconcompiler/) Python API. Once setup is complete, automated compilation can be initiated with a single line run command.

Logik depends on the [Logiklib](https://github.com/siliconcompiler/logiklib) which contains the architecture descriptions and device setup files needed to drive the Logik flow.

![logik_flow](https://raw.githubusercontent.com/siliconcompiler/logik/main/images/logik_flow.svg)

Logik supports most of the features you would expect in a commercial proprietary FPGA tool chain.

| Feature                  | Status |
|--------------------------|--------|
| Design languages         | SystemVerilog, Verilog, VHDL
| ALU synthesis            | Supported
| RAM synthesis            | Supported
| Timing constraints (SDC) | Supported
| Pin Constraints (PCF)    | Supported
| Bitstream generation     | Supported
| IP management            | Supported
| Remote compilation       | Supported
| Multi-clock designs      | Supported
| Supported devices        | Logiklib devices

## Getting Started

The Logik tool chain is available through PyPi and can be installed using pip.

```sh
python -m pip install --upgrade logik
```

All open source FPGA pre-requisites can be installed via the SiliconCompiler `sc-install` utility.

```sh
sc-install -group fpga
```

The following example illustrate some essential Logik features. For complete documentation of all options available, see the [SiliconCompiler project](https://github.com/siliconcompiler/siliconcompiler/blob/main/README.md).

```python

from siliconcompiler import Chip
from logik.flows import logik_flow
from logiklib.demo.K4_N8_6x6 import K4_N8_6x6


def hello_adder():

    # Create compilation object
    chip = Chip('adder')
    chip.create_cmdline(switchlist=['-remote'])

    # Specify design sources
    chip.input('adder.v')

    # Specify pin constraints
    chip.input('adder.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)

    # Select target fpga
    chip.set('fpga', 'partname', 'K4_N8_6x6')

    # Load target settings
    chip.set('option', 'flow', 'logik_flow')
    chip.use(logik_flow)
    chip.use(K4_N8_6x6)

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()

if __name__ == "__main__":
    hello_adder()

```

## Examples

* [Ethernet](./examples/eth_mac_1g/eth_mac_1g.py): Ethernet MAC compiled for `z1000` architecture
* [Adder](examples/adder/adder.py): Small adder example compiled for a virtual VPR architecture.

## Documentation

* [Logik Documentation](https://logik.readthedocs.io/en/latest/)
* [SiliconCompiler Documentation](https://docs.siliconcompiler.com/en/stable/)


## Installation

Logik is available as wheel packages on PyPI for macOS, Windows and Linux platforms. For a Python 3.8-3.12 environment, just use pip to install.

```sh
python -m pip install --upgrade logik
```

Running natively on your local machine will require installing a number of prerequisites:

* [Silicon Compiler](https://github.com/siliconcompiler/siliconcompiler): Hardware compiler framework
* [Slang](https://github.com/MikePopoloski/slang): SystemVerilog Parser
* [GHDL](https://ghdl.github.io/ghdl/): VHDL parser
* [Yosys](https://github.com/YosysHQ/yosys): Logic synthesis
* [VPR](https://github.com/verilog-to-routing/vtr-verilog-to-routing): FPGA place and route
* [FASM](https://github.com/chipsalliance/fasm): FPGA assembly parser and generator

We recommend using the SiliconCompiler `sc-install` utility to automatically install the correct versions of all open source FPGA tool dependencies.

```sh
sc-install -group fpga
```

Detailed installation instructions can be found in the [SiliconCompiler Installation Guide](https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools).


## License

[Apache License 2.0](LICENSE)

## Issues / Bugs
We use [GitHub Issues](https://github.com/siliconcompiler/logik/issues) for tracking requests and bugs.
