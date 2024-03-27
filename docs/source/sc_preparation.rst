Preparing the Silicon Compiler Run Script
=========================================

Developing a Silicon Compiler run script for RTL-to-bitstream flow execution follows the same fundamental approach as developing a script for any Silicon Compiler flow execution.  Additional resources for understanding Silicon Compiler fundamentals are available at

For most designs, the example Silicon Compiler run scripts provided with <tool_name> can be used as templates for creating your own.  The commands used in these examples and the general method for constructing run scripts are described below.

Constructing a Silicon Compiler run script can be broken down into the following steps:

* Import modules
* Create main function
* Create chip object
* Select part name
* Register packages (if needed)
* Import libraries (if needed)
* Set input source files
* Set timing constraints
* Set pin constraints
* Add options
* Add execution calls
  

Import modules
--------------

All Silicon Compiler run scripts are pure Python scripts that import Silicon Compiler functionality like any other Python module.  Similarly, the <tool_name> RTL-to-bitstream flow is enabled as a set of Python modules that integrate to Silicon Compiler.

The minimum import requirements in a <tool_name> Silicon Compiler run script are:

::

   import siliconcompiler
   from ebrick_fpga_cad.targets import ebrick_fpga_target


Additional module imports may be required depending on project-specific requirements.

Create Main Function
--------------------

Since the Silicon Compiler run script is just a Python script, executing it from the command-line requires the same infrastructure as any other Python script.  In most design flows, the most convenient way to enable this will be to simply encapsulate the script in a main() function:

In Python, an executable main() function is implemented with the following code:

::

   def main(<main_function_parameters (optional)>):

       #Insert your main function here

   if __name__ == "__main__":
       main()

Experienced Python programmers may prefer to use their own scripting methodology for executing the script instead of the above.  Any approach that conforms to both Python and Silicon Compiler requirements should work.

Create Chip Object
------------------

Silicon Compiler design information is encapsulated in a Python class called Chip.  An instance of this class is required for all Silicon Compiler run scripts and is commonly referred to as the chip object.

The Chip class constructor requires one parameter:  the name of the top level module in your RTL design.  A complete Chip instantiation takes the form

::

   chip = siliconcompiler.Chip('<your_top_module_name>')


Nearly all components of a Silicon Compiler run script are calls to member functions of this class instance; it should be the first (or nearly the first) line in your main function.

Throughout this documentation, "chip" will be used to refer to the Chip class instance.  However, there is no requirement that the instance be assigned to this variable name.

Select part name
----------------

.. note::

   As of this writing, the only part name that is enabled for use is "ebrick_fpga_demo"

In your Silicon Compiler run script, include the following call

::

   chip.set('fpga', 'partname', 'ebrick_fpga_demo')

to select the ebrick_fpga_demo part as your selected part name.

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

.. note::

   This method is also used for importing Zero ASIC IP blocks (e.g. UMI)


Set input source files
----------------------

All HDL source files must be added to the Silicon Compiler chip object for inclusion.  For each HDL file, include the following call in your Silicon Compiler run script

::

    chip.input('rtl', 'verilog', <your_hdl_file_name>)

for Verilog source.

Limited support is provided for VHDL and SystemVerilog inputs.  The limits to support are imposed by the capabilities of GHDL and sv2v, respectively, for translating VHDL and SystemVerilog into Verilog-2005 HDL that can be parsed by Yosys.

::

    chip.input('rtl', '', '<your_vhdl_file_name>')

::

    chip.input('rtl', '', '<your_system_verilog_file_name>')

For large designs, it may be convenient to organize your HDL files into a directory tree that is processed using Python functions, so that the above calls can be embedded in loops.

Adding source files from a registered package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When importing IP from a package in the Silicon Compiler package registry, the same function calls are used as described above, but it is also necessary to specify the package name.  The call takes the form:

::

    chip.input('rtl', '', '<your_system_verilog_file_name>', package='<package_name>')


Set Timing Constraints
----------------------

Timing constraints must be provided in a single SDC file.  The SDC file must be added to the Silicon Compiler chip object for inclusion.  Include the call

::

    chip.add('input', 'constraint', 'sdc', '<your_sdc_file_name>')

in your Silicon Compiler run script

Set Pin Constraints
--------------------

Pin constraints may be provided in one of two files:

* A JSON pin constraints file
* A VPR XML placement constraints file

.. note::

   If you need to specify placement constraints for design blocks in addition to specifying pin constraints, the XML placement constraints file must be used.

JSON Pin Constraint Specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The JSON pin constraint file is unique to this flow.  For additional information on creating the JSON pin constraint file, see []().

The XML placement constraints file must be added to the Silicon Compiler chip object for inclusion.  Include the call

::

   chip.add('input', 'constraint', 'pinmap', '<your_json_file_name>')

in your Silicon Compiler run script

VPR XML Placement Constraint Specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VPR XML placement constraints are portable to any VPR-based place and route flow.  For additional information on creating a VPR XML placement constraint file, see ()[].

The XML placement constraints file must be added to the Silicon Compiler chip object for inclusion.  Include the call

::
   
   chip.add('input', 'constraint', '', '<your_xml_file_name>')

in your Silicon Compiler run script.

Add Options
-----------

Numerous options can be added to your run script to control Silicon Compiler behavior or configure tools in the RTL-to-bitstream flow to behave as desired.

Any compiler directives that are required for HDL synthesis should be specified as Silicon Compiler options.  These are furnished with Chip class member function calls of the form

::

   chip.add('option', 'define', <compiler_directive>)

For complete Silicon Compiler option specifications, refer to `Silicon Compiler's documentation for supported option settings <https://docs.siliconcompiler.com/en/stable/reference_manual/schema.html#param-option-ref>`_.

Add Execution Calls
-------------------

The final two lines of every run script should be the same:

::
   
   chip.run()
   chip.summary()
   
The run() call invokes the RTL-to-bitstream flow with all settings specified.  The summary() call reports results of the run in tabular form.  Included in the summary results are key design metrics such as FPGA resource utilization and tool execution runtimes.
