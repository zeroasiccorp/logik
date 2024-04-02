Installing Required Software
============================

There are two ways to install the above software tools:
    1. Run within the Silicon Compiler tools docker image
    2. Build from source yourself

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

Silicon Compiler's documentation provides reference install scripts for tools used in its flows.  These can be used as startpoints for developing install scripts for your particular system and are available at `https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools <https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools>`_

Additionally, the external links page in this documentation points to documentation for open source software used in the flow.  Each of these software tools maintains its own installation instructions.  For the most up-to-date information on each software's installation procedure, its own documentation should be consulted.




