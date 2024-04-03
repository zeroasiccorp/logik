Preparing the Silicon Compiler Run Script
=========================================

Developing a Silicon Compiler run script for RTL-to-bitstream flow execution follows the same fundamental approach as developing a script for any Silicon Compiler flow execution.  Additional resources for understanding Silicon Compiler fundamentals are available at `docs.siliconcompiler.com <https://docs.siliconcompiler.com/en/stable>`_

For most designs, the example Silicon Compiler run scripts provided with <tool_name> can be used as templates for creating your own.  The commands used in these examples and the general method for constructing run scripts are described below.

Constructing a Silicon Compiler run script can be broken down into the following steps:

* :ref:`import_modules`
* :ref:`Create_main_function`
* :ref:`Create_chip_object`
* :ref:`Select_part_name`
* :ref:`Register_packages`
* :ref:`Import_libraries`
* :ref:`Set_input_source_files`
* :ref:`Set_timing_constraints`
* :ref:`Set_pin_constraints`
* :ref:`Add_options`
* :ref:`Configure_remote_execution`
* :ref:`Add_execution_calls`
  
.. _import_modules:

Import Modules
--------------

All Silicon Compiler run scripts are pure Python scripts that import Silicon Compiler functionality like any other Python module.  Similarly, the <tool_name> RTL-to-bitstream flow is enabled as a set of Python modules that integrate to Silicon Compiler.

The minimum import requirements in a Logik Silicon Compiler run script are:

::

   import siliconcompiler
   from logik.targets import logik_target


Additional module imports may be required depending on project-specific requirements.

.. _Create_main_function:

Create Main Function
--------------------

Since the Silicon Compiler run script is just a Python script, executing it from the command line requires the same infrastructure as any other Python script.  In most design flows, the most convenient way to enable this will be to simply encapsulate the script in a main() function:

In Python, an executable main() function is implemented with the following code:

::

   def main(<main_function_parameters (optional)>):

       #Insert your main function here

   if __name__ == "__main__":
       main()

Experienced Python programmers may prefer to use their own scripting methodology for executing the script instead of the above.  Any approach that conforms to both Python and Silicon Compiler requirements should work.

.. _Create_chip_object:

Create Chip Object
------------------

Silicon Compiler design information is encapsulated in a Python class called Chip.  An instance of this class is required for all Silicon Compiler run scripts and is commonly referred to as the chip object.

The Chip class constructor requires one parameter:  the name of the top level module in your RTL design.  A complete Chip instantiation takes the form

::

   chip = siliconcompiler.Chip('<your_top_module_name>')


Nearly all components of a Silicon Compiler run script are calls to member functions of this class instance; it should be the first (or nearly the first) line in your main function.

Throughout this documentation, "chip" will be used to refer to the Chip class instance.  However, there is no requirement that the instance be assigned to this variable name.

.. _Select_part_name:

Select Part Name
----------------

Silicon Compiler associates each FPGA/eFPGA architecture with a unique ID called a part name.

.. note::

   As of this writing, the only part name that is enabled for use is "logik_demo"

In your Silicon Compiler run script, include the following call

::

   chip.set('fpga', 'partname', 'logik_demo')

to select the logik_demo part as your selected part name.

.. _Register_packages:

Register Packages (if needed)
-----------------------------

Designs with dependencies on third-party or packaged IP from previous projects may require a method for importing design IP from a source other than local working directories.  In Silicon Compiler, such imports are supported via the Silicon Compiler package registry, and the import process is referred to as registering a package.

Registering a package is enabled with a dedicated Chip class member function called register_package_source().  For complete details on this function, refer to `Silicon Compiler's documentation of the register_package_source() function <https://docs.siliconcompiler.com/en/stable/reference_manual/core_api.html#siliconcompiler.Chip.register_package_source>`_.

An example use case for the package registry is shown below, outlining how to import a public Github repository so that its contents can be used as a package within Silicon Compiler.  In this example, three parameters are provided to the register_package_source function:  name, path, and ref.  Name specifies a package name to be used when referring to the package elsewhere in code.  Path specifies where Silicon Compiler can obtain the package; in this case, the package is obtained through Github.  ref specifies to Silicon Compiler that the cloned Github repository should be checked out at a particular commit hash.  Specifying ref is not necessary if the package is to be cloned from github on its main branch.

::

    chip.register_package_source(
        name='picorv32',
        path='git+https://github.com/YosysHQ/picorv32.git',
        ref='a7b56fc81ff1363d20fd0fb606752458cd810552')

.. _Import_libraries:

Set Input Source Files
----------------------

All HDL source files must be added to the Silicon Compiler chip object for inclusion.  For each HDL file, include the following call in your Silicon Compiler run script

::

    chip.input(<your_hdl_file_name>)

Support is provided for Verilog, VHDL and SystemVerilog inputs.

.. note::

   Mixed-language flows are not yet supported.  All HDL source files must be written in the same language.

When using VHDL, it is required to add

::

   chip.set('option', 'frontend', 'vhdl')
   
to your run script to trigger Silicon Compiler to execute ghdl prior to running synthesis.

When using SystemVerilog, it is required to add

::

   chip.set('option', 'frontend', 'systemverilog')

to your run script to trigger Silicon Compiler to execute sv2v prior to running synthesis.

When using Verilog, the default frontend option, Surelog, is used, and no function call is required to enable it.

.. note::

   Silicon Compiler supports additional front end options, including flows for high-level synthesis.  For all front end compilation considerations not described above, please consult `Silicon Compiler Frontend documentation <https://docs.siliconcompiler.com/en/stable/user_guide/tutorials/hw_frontends.html>`_

For large designs, it may be convenient to organize your HDL files into a directory tree that is processed using Python functions, so that the above calls can be embedded in loops.

.. _Set_input_source_files:

Adding Source Files From a Registered Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When importing IP from a package in the Silicon Compiler package registry, the same function calls are used as described above, but it is also necessary to specify the package name.  The call takes the form:

::

    chip.input('<your_file_name>', package='<package_name>')

.. _Set_timing_constraints:

Set Timing Constraints
----------------------

.. note::

   The demo architecture provided with this distrbution implements a unit delay model.  Provided examples demonstrate the RTL-to-bitstream flow without an SDC file.  Examples that include SDC files are planned for a future release.

Timing constraints must be provided in a single SDC file.  The SDC file must be added to the Silicon Compiler chip object for inclusion.  Include the call

::

    chip.add('input', 'constraint', 'sdc', '<your_sdc_file_name>')

in your Silicon Compiler run script.

.. note::

   If no SDC file is provided, the flow will still run to completion.  Timing analysis will be disabled during the place and route steps.

.. _Set_pin_constraints:

Set Pin Constraints
--------------------

Pin constraints may be provided in one of two files:

* A JSON pin constraints file (PCF)
* A VPR XML placement constraints file

.. note::

   If you need to specify placement constraints for design logic blocks in addition to specifying pin constraints, the XML placement constraints file must be used.

JSON Pin Constraint Specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The JSON pin constraint file is unique to this flow.  For additional information on creating the JSON pin constraint file, see :doc:`pin_constraints`.

The JSON placement constraints file must be added to the Silicon Compiler chip object for inclusion.  Include the call

::

   chip.input('<your_pcf_file_name>')

If your project defines itself as a package using Silicon Compiler's package registry, specify the package name as well:

::

   chip.input('<your_pcf_file_name>', package=<your_package_name>)

in your Silicon Compiler run script

.. note::

   The .pcf file extension must be used

VPR XML Placement Constraint Specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VPR XML placement constraints are portable to any VPR-based place and route flow.  For additional information on creating a VPR XML placement constraint file, see `VPR's documentation for placement constraints <https://docs.verilogtorouting.org/en/latest/vpr/placement_constraints/>`_.

The XML placement constraints file must be added to the Silicon Compiler chip object for inclusion.  Include the call

::
   
   chip.add('input', 'constraint', 'pins', '<your_xml_file_name>')

in your Silicon Compiler run script.

.. _Add_options:

Add Options
-----------

Numerous options can be added to your run script to control Silicon Compiler behavior or configure tools in the RTL-to-bitstream flow to behave as desired.  For complete Silicon Compiler option specifications, refer to `Silicon Compiler's documentation for supported option settings <https://docs.siliconcompiler.com/en/stable/reference_manual/schema.html#param-option-ref>`_.

In particular, any compiler directives that are required for HDL synthesis should be specified as Silicon Compiler options.  These are furnished with Chip class member function calls of the form

::

   chip.add('option', 'define', <compiler_directive>)


.. _Configure_remote_execution:
   
Configure Remote Execution (optional)
-------------------------------------

Silicon Compiler supports job submission to remote servers.

There are multiple ways to enable this execution model.  Consult `Silicon Compiler remote processing <https://docs.siliconcompiler.com/en/stable/development_guide/remote_processing.html>`_ documentation for details.

.. _Add_execution_calls:

Add Execution Calls
-------------------

The final two lines of every run script should be the same:

::
   
   chip.run()
   chip.summary()
   
The run() call invokes the RTL-to-bitstream flow with all settings specified.  The summary() call reports results of the run in tabular form.  Included in the summary results are key design metrics such as FPGA resource utilization and tool execution runtimes.
