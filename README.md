![Logik](https://raw.githubusercontent.com/zeroasiccorp/logik/main/images/logik_logo_with_text.png)

[![Regression](https://github.com/zeroasiccorp/logik/actions/workflows/regression.yml/badge.svg)](https://github.com/zeroasiccorp/logik/actions/workflows/regression.yml)
[![Lint](https://github.com/zeroasiccorp/logik/actions/workflows/lint.yml/badge.svg)](https://github.com/zeroasiccorp/logik/actions/workflows/lint.yml)

-----------------------------------------------------------------------------------

Logik is an open source FPGA toolchain that fully automates converting RTL to bits, including synthesis, placement, routing, bitstream generation, and analysis. Users enter design sources, constraints, and compile options through a simple [SiliconCompiler](https://github.com/siliconcompiler/siliconcompiler/) Python API. Once setup is complete, automated compilation can be initiated with a single line run command.

![logik_flow](https://raw.githubusercontent.com/zeroasiccorp/logik/main/images/logik_flow.svg)

Logik supports most of the features you would expect in a commercial proprietary FPGA tool chain.

| Feature                  | Status |
|--------------------------|--------|
| Design languages         | Verilog, SystemVerilog, VHDL
| ALU synthesis            | Supported
| RAM synthesis            | Supported
| Timing constraints (SDC) | Supported
| Pin Constraints (PCF)    | Supported
| Bitstream generation     | Supported
| IP management            | Supported
| Remote compilation       | Supported
| Multi-clock designs      | In progress
| FPGA devices             | ZA

## Getting Started

The Logik project is available through PyPi and can be installed using pip. If you want to run locally on your machine, you will need to [install all of the pre-requisites](#installation) or launch the [Logik Docker image](#running-docker).

```sh
python -m pip install --upgrade logik
```

The following example illustrate some essential Logik features. For complete documentation of all options available, see the [SiliconCompiler project](https://github.com/siliconcompiler/siliconcompiler/blob/main/README.md).

```python
from siliconcompiler import Chip
from logik.targets import logik_target

def hello_adder():

    # Create compilation object
    chip = Chip('adder')

    # Specify design sources
    chip.input('adder.v')

    # Specify pin constraints
    chip.input('adder.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)
    chip.set('option', 'remote', True)

    # Select target fpga
    chip.set('fpga', 'partname', 'logik_demo')

    # Load target settings
    chip.load_target(logik_target)

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()

if __name__ == "__main__":
    hello_adder()
```

This code can be run with `./adder.py -remote` in the [examples/adder](examples/adder/) directory, resulting in an FPGA bitstream at `build/adder/job0/convert_bitstream/0/outputs/adder.bin`.

To test out the generated bitstream, you can upload it to an emulated FPGA device running in the Zero ASIC [Digital Twin Platform](https://www.zeroasic.com/emulation?demo=fpga).


## More Examples

* [UMI "Hello World"](./examples/umi_hello/)
* [UMI FIR Filter](./examples/umi_fir_filter)
* [EBRICK demo](./examples/ebrick_demo_fpga/)

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
* [Yosys](https://github.com/YosysHQ/yosys): Logic synthesis
* [VPR](https://github.com/verilog-to-routing/vtr-verilog-to-routing): FPGA place and route
* [GHDL](https://ghdl.github.io/ghdl/): VHDL parser
* [Surelog](https://github.com/chipsalliance/Surelog): SystemVerilog parser
* [FASM](https://github.com/chipsalliance/fasm): FPGA assembly parser and generator

Automated Ubuntu based install scripts are included for convenience within the SiliconCompiler project. Detailed instructions for installing all tools can be found in the [SiliconCompiler Installation Guide](https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools).


## Running Docker

A [Docker image](https://github.com/siliconcompiler/siliconcompiler/pkgs/container/sc_runner) is provided for users who wish to avoid the installation of the pre-requisite tools. The following command starts a new container from that image and maps the local directory `sc_work` to the path `/sc_work` in the container.

```sh
docker run -it -v "${PWD}/sc_work:/sc_work" ghcr.io/siliconcompiler/sc_runner:latest
```


## License

[MIT](LICENSE)

## Issues / Bugs
We use [GitHub Issues](https://github.com/zeroasiccorp/logik/issues) for tracking requests and bugs.
