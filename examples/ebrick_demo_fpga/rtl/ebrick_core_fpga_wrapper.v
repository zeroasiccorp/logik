/*******************************************************************************
 * Copyright 2024 Zero ASIC Corporation
 *
 * Licensed under the MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY,WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * ----
 *
 ******************************************************************************/

//This file puts a wrapper around the ebrick_core to adapt it so that it can
//be mapped to valid ebrick-fpga core pins for placement, routing, and pinout
//to ebrick pins

module ebrick_core_fpga_wrapper
  # (
     parameter TARGET = "DEFAULT", // technology target
     parameter W = 2,              // #clinks (width) (1,2,3,4,5)
     parameter H = 2,              // #clinks (height) (1,2,3,4,5)
     parameter CW = 32,            // umi packet width
     parameter AW = 64,            // address space width
     parameter RW = 32,            // register space width
     parameter DW = 64,            // umi data width
     parameter IDW = 16,           // chipid width
     parameter NPT = 2,            // pass-through pins per clink
     parameter NGPIO = 16,         // GPIOs per clink/2mm side of 2D
     parameter NAIO = 2,           // analog io per clink
     // Derived parameters
     parameter W2 = W/2,
     parameter H2 = H/2
     ) (
	// The ebrick_fpga_demo FPGA offers three clock signals.
	// Since the ebrick core has a total of five, we must pick
	// which three to emulate on the FPGA.  Below assign statements
	// will map the three FPGA clocks to clk and two auxclk signals
	input [2:0] 		fpga_clk,

	// global ebrick controls (from clink0/ebrick_regs/bus)
	// for demonstration purposes, many of these will be tied
	// off.  When mapping to the ebrick_fpga_demo architecture
	// each of these pins would need to consume a GPIO, so
	// bringing these out as ports is relatively costly since
	// only 64 GPIOs are available
	input 			nreset, // async active low reset
	input 			go, // 1=start/boot core
	input 			testmode, // 1=connect brick IO directly to core.
	// input [1:0] 		chipletmode, // 00=150um,01=45um,10=10um,11=1um
	// input [1:0] 		chipdir, // brick direction (wrt fabric)
	// input [W*H*IDW-1:0] 	chipid, // unique brick id
	// input [63:0] 	irq_in, // interrupts vector to the core
	// output [63:0] 	irq_out, // interrupts vector to the ebrick cpu

	// JTAG interface (from a core or looped in->out)
	input 			jtag_tck,
	input 			jtag_tms,
	input 			jtag_tdi,
	output 			jtag_tdo,
	output 			jtag_tdo_oe,

	// general controls
	// Many of the control signals are reserved for ebrick template
	// use, and another five are reserved for ebrick-fpga control
	// signals.  This leaves relatively few for user use in this scheme.
	// For now to save GPIOs, omit the control bus altogether.
	// input [RW-1:0] 	ctrl, // generic control vector
	// Similarly most status bits are consumed either by ebrick-fpga
	// or ebrick template.  Rather than spend GPIOs on these, spend them
	// on other signals instead
	// output [RW-1:0] 	status, // generic status
	// initdone is not used in ebrick_demo and can be omitted from the
	// wrapper port list accordingly
	// output 			initdone, // generic status
	// Choose not to bring out the test interface for now; use
	// JTAG instead
	// input 			test_scanmode,
	// input 			test_scanenable,
	// input 			test_scanin,
	// output 			test_scanout,

	// Host ports (one per CLINK)
	// Since the demo architecture has only three UMI ports
	// because the other is reserved for bitstream loading,
	// bring out three of the 4 UMI ports in this design
	output [(W*H-1)-1:0] 	uhost_req_valid,
	output [(W*H-1)*CW-1:0] uhost_req_cmd,
	output [(W*H-1)*AW-1:0] uhost_req_dstaddr,
	output [(W*H-1)*AW-1:0] uhost_req_srcaddr,
	output [(W*H-1)*DW-1:0] uhost_req_data,
	input [(W*H-1)-1:0] 	uhost_req_ready,
	input [(W*H-1)-1:0] 	uhost_resp_valid,
	input [(W*H-1)*CW-1:0] 	uhost_resp_cmd,
	input [(W*H-1)*AW-1:0] 	uhost_resp_dstaddr,
	input [(W*H-1)*AW-1:0] 	uhost_resp_srcaddr,
	input [(W*H-1)*DW-1:0] 	uhost_resp_data,
	output [(W*H-1)-1:0] 	uhost_resp_ready,

	// Device ports (one per CLINK)
	input [(W*H-1)-1:0] 	udev_req_valid,
	input [(W*H-1)*CW-1:0] 	udev_req_cmd,
	input [(W*H-1)*AW-1:0] 	udev_req_dstaddr,
	input [(W*H-1)*AW-1:0] 	udev_req_srcaddr,
	input [(W*H-1)*DW-1:0] 	udev_req_data,
	output [(W*H-1)-1:0] 	udev_req_ready,
	output [(W*H-1)-1:0] 	udev_resp_valid,
	output [(W*H-1)*CW-1:0] udev_resp_cmd,
	output [(W*H-1)*AW-1:0] udev_resp_dstaddr,
	output [(W*H-1)*AW-1:0] udev_resp_srcaddr,
	output [(W*H-1)*DW-1:0] udev_resp_data,
	input [(W*H-1)-1:0] 	udev_resp_ready,

	// To fully emulate the GPIO at the core level
	// requires three FPGA GPIOs per ebrick_core GPIO
	// --one each for input, output, and output enable--
	// since the FPGA GPIOs are unidirectional once
	// a bitstream is loaded.  Bring out just north
	// GPIOs for now and leave the rest out of the port
        // list so we can spend 16 FPGA GPIOs on other signals
	output [W2*NGPIO-1:0] 	no_txgpio,
	output [W2*NGPIO-1:0] 	no_txgpiooe,
	input [W2*NGPIO-1:0] 	no_rxgpio

	// output [H2*NGPIO-1:0] 	ea_txgpio,
	// output [H2*NGPIO-1:0] 	ea_txgpiooe,
	// input [H2*NGPIO-1:0] 	ea_rxgpio,

	// output [W2*NGPIO-1:0] 	so_txgpio,
	// output [W2*NGPIO-1:0] 	so_txgpiooe,
	// input [W2*NGPIO-1:0] 	so_rxgpio,

	// output [H2*NGPIO-1:0] 	we_txgpio,
	// output [H2*NGPIO-1:0] 	we_txgpiooe,
	// input [H2*NGPIO-1:0] 	we_rxgpio,

	// Bidirectional/analog ports do not have FPGA equivalents; omit
	// inout [W2*NAIO-1:0]   no_analog, // analog interface through padring
	// inout [H2*NAIO-1:0]   ea_analog, // analog interface through padring
	// inout [W2*NAIO-1:0]   so_analog, // analog interface through padring
	// inout [H2*NAIO-1:0]   we_analog, // analog interface through padring
	// inout [W*H*NPT-1:0]   pad_nptn, // pass through inputs
	// inout [W*H*NPT-1:0]   pad_eptn, // pass through inputs
	// inout [W*H*NPT-1:0]   pad_sptn, // pass through inputs
	// inout [W*H*NPT-1:0]   pad_wptn, // pass through inputs
	// inout [W*H*NPT-1:0]   pad_nptp, // pass through inputs
	// inout [W*H*NPT-1:0]   pad_eptp, // pass through inputs
	// inout [W*H*NPT-1:0]   pad_sptp, // pass through inputs
	// inout [W*H*NPT-1:0]   pad_wptp, // pass through inputs

	// Memory macro control signals are tied off internal to the FPGA core;
	// omit from this port list
	// input [7:0] 	      csr_rf_ctrl,
	// input [7:0] 	      csr_sram_ctrl,

	// Supplies do not have functional meaning as FPGA ports; leave them out
	// input 	      vss,
	// input 	      vdd,
	// input 	      vddx,
	// input [3:0] 	      vcc,
	// input [3:0] 	      vdda  
    );

   wire 			clk;
   wire [3:0] 			auxclk;
   
   //Do the mapping of the clocks here
   
   assign clk = fpga_clk[0];
   assign auxclk[1] = fpga_clk[1];
   assign auxclk[2] = fpga_clk[2];
      
   ebrick_core #(.TARGET(TARGET),
                 .W(W),
                 .H(H),
                 .NPT(NPT),
                 .NAIO(NAIO),
                 .CW(CW),
                 .RW(RW),
                 .DW(DW),
                 .IDW(IDW),
                 .AW(AW))
   ebrick_core(// Outputs
	       .initdone          (),
               .irq_out           (),
               .jtag_tdo          (jtag_tdo),                      
               .jtag_tdo_oe       (jtag_tdo_oe),                      
               .status            (),
               .test_scanout      (),
               .uhost_req_valid   (uhost_req_valid),
               .uhost_req_cmd     (uhost_req_cmd),
               .uhost_req_dstaddr (uhost_req_dstaddr),
               .uhost_req_srcaddr (uhost_req_srcaddr),
               .uhost_req_data    (uhost_req_data),
               .uhost_resp_ready  (uhost_resp_ready),
               .udev_req_ready    (udev_req_ready),
               .udev_resp_valid   (udev_resp_valid),
               .udev_resp_cmd     (udev_resp_cmd),
               .udev_resp_dstaddr (udev_resp_dstaddr),
               .udev_resp_srcaddr (udev_resp_srcaddr),
               .udev_resp_data    (udev_resp_data),
               .no_txgpio         (no_txgpio),
               .no_txgpiooe       (no_txgpiooe),
               .ea_txgpio         (),
               .ea_txgpiooe       (),
               .so_txgpio         (),
               .so_txgpiooe       (),
               .we_txgpio         (),
               .we_txgpiooe       (),
               // Inouts are not allowed in VPR, leave them all unconnected
               .no_analog         (), 
               .ea_analog         (), 
               .so_analog         (), 
               .we_analog         (), 
               .pad_nptn          (), 
               .pad_eptn          (), 
               .pad_sptn          (), 
               .pad_wptn          (), 
               .pad_nptp          (), 
               .pad_eptp          (), 
               .pad_sptp          (), 
               .pad_wptp          (), 
               // Inputs
               .clk               (clk),
               .auxclk            (auxclk),
               .nreset            (nreset),
               .go                (go),
               .testmode          (testmode),
               .chipletmode       ('h0),
               .chipdir           ('h0),
               .chipid            ('h0),
               .irq_in            ('h0),
               .jtag_tck          (jtag_tck),
               .jtag_tms          (jtag_tms),
               .jtag_tdi          (jtag_tdi),
               .ctrl              ('h0),
               .test_scanmode     (1'b0),
               .test_scanenable   (1'b0),
               .test_scanin       (1'b0),
               .uhost_req_ready   (uhost_req_ready),
               .uhost_resp_valid  (uhost_resp_valid),
               .uhost_resp_cmd    (uhost_resp_cmd),
               .uhost_resp_dstaddr(uhost_resp_dstaddr),
               .uhost_resp_srcaddr(uhost_resp_srcaddr),
               .uhost_resp_data   (uhost_resp_data),
               .udev_req_valid    (udev_req_valid),
               .udev_req_cmd      (udev_req_cmd),
               .udev_req_dstaddr  (udev_req_dstaddr),
               .udev_req_srcaddr  (udev_req_srcaddr),
               .udev_req_data     (udev_req_data),
               .udev_resp_ready   (udev_resp_ready),
               .no_rxgpio         (no_rxgpio),
               .ea_rxgpio         ('h0),
               .so_rxgpio         ('h0),
               .we_rxgpio         ('h0),
               .csr_rf_ctrl       ('h0),
               .csr_sram_ctrl     ('h0),
               .vss               (1'b0),
               .vdd               (1'b1),
               .vddx              (1'b1),
               .vcc               (1'b0),
               .vdda              (1'b1)
	       );   

endmodule // ebrick_core_wrapper

