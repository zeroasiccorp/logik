Demo Edition
============

Welcome to the demo edition of <name>.  In this edition, the following features are showcased:

* RTL to bitstream automation flow for Zero ASIC FPGA/eFPGA architectures, powered by `Silicon Compiler <https://www.siliconcompiler.com>`_
* Example Zero ASIC eFPGA architecture with the following resources:

  +----------------------------------------------------------+--------+
  | 4-input LUTs                                             | 6576   |
  +----------------------------------------------------------+--------+
  | Registers                                                | 6576   |
  +----------------------------------------------------------+--------+
  | GPIOs                                                    | 64     |
  +----------------------------------------------------------+--------+
  | `UMI Interfaces <https://github.com/zeroasiccorp/umi>`_  | 3      |
  +----------------------------------------------------------+--------+
  | 4KB Block RAMs                                           | 16     |
  +----------------------------------------------------------+--------+
  | Multiply-Add Engines (MAEs)                              | 16     |
  +----------------------------------------------------------+--------+

* Example designs for reference in adopting the flow
* Tutorials for running the flow and seeing bitstream output run on Zero ASIC's <name> platform.
* Documentation providing step-by-step guidance for setup and execution of the flow
  
Documentation Table of Contents
===============================

.. toctree::
    :maxdepth: 2
    :caption: Usage
    
    prerequisites
    tool_installations
    design_preparation
    sc_preparation
    execution

.. toctree::
    :maxdepth: 1
    :caption: References

    timing_constraints	      
    pin_constraints
    template_constraints
    external_links
    

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
