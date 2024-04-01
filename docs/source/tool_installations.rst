Installing Required Software
============================

There are two ways to install the above software tools:
    1. Run within the Silicon Compiler tools docker image
    2. Build from source yourself.  This usually requires checking out the qualified versions of the source repositories, which are documented in instructions below

Silicon Compiler Tools Docker Image Setup
-----------------------------------------

First, install Docker according to the instructions for your operating system:

* `Linux Docker installation <https://docs.docker.com/desktop/install/linux-install/>`_
* `macOS Docker installation <https://docs.docker.com/desktop/install/mac-install/>`_
* `Windows Docker installation <https://docs.docker.com/desktop/install/windows-install/>`_

Once Docker is installed, launch the Docker Desktop application.

* Ubuntu: `Ctrl`-`Alt`-`T` or run the Terminal application from the Dash
* macOS: `Cmd-Space` to open Spotlight, then type `Terminal` and press `Enter`
* Windows: Open `Windows PowerShell` from the Start menu.

::
   
   docker run -it -v "${PWD}/sc_work:/sc_work" ghcr.io/siliconcompiler/sc_runner:latest
       
Building Software From Source
-----------------------------

Several resources are offered to assist in the installation process when tools need to be built from source.

The most complete reference for installing open source software used in this flow is available in Silicon Compiler's documentation

`https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools <https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools>`_

Some notes regarding individual software tool installations are provided below.

Surelog Installation
^^^^^^^^^^^^^^^^^^^^

Typically, installing Surelog from source is not necessary.  When Silicon Compiler is installed via pip, Surelog is installed with it.

If your system requirements necessitate installing Surelog, the following recipe can be used:

* Clone the `Surelog Github repository <https://github.com/chipsalliance/Surelog>`_
* Check out the current qualified version:  `git checkout v1.82`
* Follow the `Surelog build instructions <https://github.com/chipsalliance/Surelog?tab=readme-ov-file#build-instructions-and-test>`_
* If make install is not used, add the path to the surelog executable to your PATH environment variable

Yosys Installation
^^^^^^^^^^^^^^^^^^

* Clone the `Yosys Github repository <https://github.com/YosysHQ>`_
* Check out the current qualified version:

::
   
   git checkout yosys-0.39
     
* Follow the `Yosys build instructions <https://github.com/YosysHQ/yosys?tab=readme-ov-file#installation>`_
* If make install is not used, add the path to the yosys executable to your PATH environment variable

VPR Installation
^^^^^^^^^^^^^^^^

* Clone the `VPR Github repository <https://github.com/verilog-to-routing/vtr-verilog-to-routing/tree/master>`_
* Check out the current qualified version

::
   
   git checkout c4156f225c7a292c5768444631ca053ea7473428
   
* Follow the `VPR build instructions <https://github.com/verilog-to-routing/vtr-verilog-to-routing/blob/master/BUILDING.md>`_
* If make install is not used, add the paths to the vpr and genfasm executables to your PATH environment variable

GHDL Installation
^^^^^^^^^^^^^^^^^

* Clone the `GHDL Github repository <https://github.com/ghdl/ghdl>`_
* Check out the current qualified version

::

   git checkout v4.0.0
   
* Follow the `GHDL build instructions <https://ghdl.github.io/ghdl/development/building/index.html#build>`_
* If make install is not used, add the path to the ghdl executable to your PATH environment variable

sv2v Installation
^^^^^^^^^^^^^^^^^

* Clone the `sv2v Github repository <https://github.com/zachjs/sv2v>`_
* Check out the current qualified version

::
   
   git checkout df01650444dca89981e866ccc9985ff8b1246a21
   
* Follow the `sv2v build instructions <https://github.com/zachjs/sv2v?tab=readme-ov-file#installation>`_
* If make install is not used, add the path to the sv2v executable to your PATH environment variable

GTKWave Installation
^^^^^^^^^^^^^^^^^^^^

This flow does not specify a qualified version of GTKWave; version 3.3.103 or higher is recommended.

When running on Ubuntu 20.04, GTKWave 3.3.103 is available as an installable package:

::

   apt-get install gtkwave

If your system requires building GTKWave from source, please consult `GTKWave documentation <https://github.com/gtkwave/gtkwave?tab=readme-ov-file#gtkwave/>` for instructions

Icarus Verilog Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Clone the `Icarus Github repository <https://github.com/steveicarus/iverilog>`_
* Check out the current qualified version

::
   
   git checkout v12_0
   
* Follow the `Icarus build instructions <https://github.com/steveicarus/iverilog?tab=readme-ov-file#buildinginstalling-icarus-verilog-from-source>`_
* If make install is not used, add the path to the icarus executable to your PATH environment variable

Verilator Installation
^^^^^^^^^^^^^^^^^^^^^^

* Clone the `Verilator Github repository <https://github.com/verilator/verilator>`_
* Check out the current qualified version

::
   
   git checkout v5.012
   
* Follow the `Verilator build instructions <https://verilator.org/guide/latest/install.html>`_
* If make install is not used, add the path to the Verilator executable to your PATH environment variable

