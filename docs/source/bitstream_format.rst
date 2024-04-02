Bitstream Formatting
====================

Bitstream data is generated in this flow in multiple formats:

* `FASM <https://fasm.readthedocs.io/en/latest/>`_ is the bitstream format supported within the Verilog-to-Routing flow.  This format is a plain text, human-readable format originally developed for `F4PGA <https://f4pga.org/>`_ and its predecessor projects.  The genfasm step in this flow emits bitstreams in FASM format.
* A JSON representation of the bitstream is generated to provide a convenient intermediate representation between the FASM-formatted bitstream and the final binary bitstream.  It is generally used for internal purposes only but can be used in addition to or instead of FASM to gain insight into the organization of configuration bits on chip.  See below for details on configuration bit organization.
* A binary representation of the bitstream is generated for delivery of the bitstream to other applications.  Generation of this file is referred to in the flow as bitstream finishing.

Understanding the details of bitstream formatting is typically necessary only for writing software drivers to perform bitstream loading for particular FPGA chips.

.. warning::

   As of this writing, the FPGA architecture supported in this flow is supplied for demonstration purposes and does not have an associated physical chip.  The following sections outline how bitstreams are organized for educational purposes only.

Working with FASM Bitstream Data
--------------------------------

A FASM file is comprised of an enumeration of "features" that are enabled or have non-zero values.  Each feature is assigned a plain-text label.

End user post-processing of the FASM file is not recommended as making use of the data requires precise knowledge of the underlying FPGA architecture.  For all considerations related to parsing the format, please consult `FASM documentation <https://fasm.readthedocs.io/en/latest/>`_

Working with JSON Bitstream Data
--------------------------------

JSON is used as the file format for storing an intermediate representation (IR) of bitstream data between FASM and binary formats.

The IR organizes the bitstream into a four-dimensional on-chip address space organized by array location.  Each bit in the bitstream can thus be indexed by an X coordinate, Y coordinate, word address, and bit index in this IR.

For each FPGA architecture supported by the flow, a bitstream map file is provided that maps FASM features into this address space.  The bitstream finishing step uses this bitstream map file to convert FASM to the IR.  The IR is then written out in JSON format.

.. warning::

   Architecture bitstream map files are cached by Silicon Compiler for use within the flow and may not be easily accessible by end users.

Working with Binary Bitstream Data
----------------------------------

The binary representation of bitstream data consolidates bitstream IR described above into a ROM-style format.  The four-dimensional address space of individual is collapsed into a one-dimensional address space of bitstream words.  The mapping is as shown in the table below

+-------------------------+------------------------------+------------------------+
| most significant bits   | next most significant bits   | least significant bits |
+-------------------------+------------------------------+------------------------+
| Y coordinate            | X coordinate                 | word address           |
+-------------------------+------------------------------+------------------------+

When mapped into this address space, bitstream words are ordered from lowest address value to highest address value.

The binary format does not specify a word size; instead, this is dictated by the FPGA Architecture.  Words are treated as binary strings that, when read left to right, are read MSB to LSB.  The packing of bitstream words into bytes in a binary file is dictated by Python's tofile() function.  Implementations of a binary bitstream file reader should account for this so that when the bitstream is read back word ordering in this address space is preserved.

To make this more concrete, consider the logik_demo architecture.  logik_demo is organized as a 37x31 array of elements.  This means that six bits are needed to represent the X coordinate and five bits are needed to represent the Y coordinate.  The number of word addresses needed at each (X,Y) coordinate in the array varies.  To make a uniform address space, the maximum required word address dictates the number of bits of word address used.  In the case of logik_demo, the maximum word address is 141, so eight bits of word address are needed.  The binary bitstream address format is thus nineteen bits wide and organized as follows:

+--------------+--------------+--------------+
| [18:14]      | [13:8]       | [7:0]        |
+--------------+--------------+--------------+
| Y coordinate | X coordinate | word address |
+--------------+--------------+--------------+

logik_demo uses 8-bit bitstream words.  The ordering of the words in the binary file thus begins with word address 0 at array coordinate (0,0) and the last word is word address 141 at array coordinate (37, 31).
