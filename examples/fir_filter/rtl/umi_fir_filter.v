//umi_fir_filter.v
//Peter Grossmann
//31 October 2023
//$Id$
//$Log$

module umi_fir_filter
  # (
     parameter CW=32,
     parameter AW=64,
     parameter DW=128,
     parameter FIR_FILTER_DATA_WIDTH = 16,
     parameter NUM_TAPS = 8,
     parameter FIR_FILTER_OUTPUT_DATA_WIDTH = 2*FIR_FILTER_DATA_WIDTH+$clog2(NUM_TAPS)
     )
   (
    input 	    clk,
    input 	    nreset,
    
    input 	    udev_req_valid,
    input [CW-1:0]  udev_req_cmd,
    input [AW-1:0]  udev_req_dstaddr,
    input [AW-1:0]  udev_req_srcaddr,
    input [DW-1:0]  udev_req_data,
    output 	    udev_req_ready,
    output 	    udev_resp_valid,
    output [CW-1:0] udev_resp_cmd,
    output [AW-1:0] udev_resp_dstaddr,
    output [AW-1:0] udev_resp_srcaddr,
    output [DW-1:0] udev_resp_data,
    input 	    udev_resp_ready    
    );

`include "umi_fir_filter_regs.vh"
   
   wire [(NUM_TAPS*FIR_FILTER_DATA_WIDTH-1):0] coeff;
   wire [(FIR_FILTER_DATA_WIDTH-1):0] 	       fir_filter_datain;
   wire [(FIR_FILTER_OUTPUT_DATA_WIDTH-1):0]   fir_filter_dataout;
   
   wire [(DW-1):0] 			       fir_filter_regs_datain;
   wire [(DW-1):0] 			       fir_filter_regs_dataout;

   wire 				       fir_filter_input_valid;
   wire 				       fir_filter_output_valid;
   
   // Memory interface
   wire [AW-1:0] 			       udev_loc_addr;    // memory address
   wire 				       udev_loc_write;   // write enable
   wire 				       udev_loc_read;    // read request
   /* verilator lint_off UNUSED */
   wire [7:0] 				       udev_loc_opcode;  // opcode
   wire [2:0] 				       udev_loc_size;    // size
   wire [7:0] 				       udev_loc_len;     // len
   wire 				       udev_loc_atomic;  // atomic request
   wire [7:0] 				       udev_loc_atype;   // atomic type
   /* verilator lint_on UNUSED */
   wire [DW-1:0] 			       udev_loc_wrdata;  // data to write
   wire [DW-1:0] 			       udev_loc_rddata;  // data response
   wire 				       udev_loc_ready;   // device is ready

   wire 				       output_store_read_enable;
   wire [(FIR_FILTER_OUTPUT_DATA_WIDTH-1):0]   output_store_dataout;

   wire 				       output_store_dataout_valid;
     
   umi_endpoint
     #(
       .REG(1),
       .CW(CW),
       .AW(AW),
       .DW(DW)
       )
   umi_receive (
		// ctrl
		.nreset(nreset),
		.clk(clk),
		// Device port
		.udev_req_valid(udev_req_valid),
		.udev_req_cmd(udev_req_cmd),
		.udev_req_dstaddr(udev_req_dstaddr),
		.udev_req_srcaddr(udev_req_srcaddr),
		.udev_req_data(udev_req_data),
		.udev_req_ready(udev_req_ready),
		.udev_resp_valid(udev_resp_valid),
		.udev_resp_cmd(udev_resp_cmd),
		.udev_resp_dstaddr(udev_resp_dstaddr),
		.udev_resp_srcaddr(udev_resp_srcaddr),
		.udev_resp_data(udev_resp_data),
		.udev_resp_ready(udev_resp_ready),
		// Memory interface
		.loc_addr(udev_loc_addr),     // memory address
		.loc_write(udev_loc_write),   // write enable
		.loc_read(udev_loc_read),     // read request
		.loc_opcode(udev_loc_opcode), // opcode
		.loc_atomic(udev_loc_atomic), // atomic request
		.loc_size(udev_loc_size),     // size
		.loc_len(udev_loc_len),       // len
		.loc_atype(udev_loc_atype),   // atomic type
		.loc_wrdata(udev_loc_wrdata), // data to write
		.loc_rddata(udev_loc_rddata), // data response
		.loc_ready(udev_loc_ready)    // device is ready
		);   


   assign fir_filter_regs_datain = udev_loc_wrdata;
   assign fir_filter_datain = udev_loc_wrdata[(FIR_FILTER_DATA_WIDTH-1):0];
   assign fir_filter_input_valid = udev_req_ready && udev_req_valid && (udev_req_dstaddr[5:4] == SAMPLE_REG_ADDR);
   				  
   assign udev_loc_rddata = (output_store_dataout_valid) ? {{(128-FIR_FILTER_OUTPUT_DATA_WIDTH){1'b0}}, output_store_dataout} : fir_filter_regs_dataout;
   assign udev_loc_ready = 1'b1;

   assign output_store_read_enable = udev_loc_read;

   umi_fir_filter_regs
     #(
       )
   fir_filter_regs (
		    .clk(clk),
		    .nreset(nreset),
		    .write(udev_loc_write),
		    .read(udev_loc_read),
		    .address(udev_loc_addr[5:4]),
		    .datain(fir_filter_regs_datain),
		    .dataout(fir_filter_regs_dataout),
		    .coeff(coeff)
		    );

   fir_filter
     #(
       .DATA_WIDTH(FIR_FILTER_DATA_WIDTH),
       .COEFF_WIDTH(FIR_FILTER_DATA_WIDTH),
       .NUM_TAPS(NUM_TAPS)
       )
   fir_filter (

	       .clk(clk),
	       .resetn(nreset),
	       .input_valid(fir_filter_input_valid),
	       .coeff(coeff),
	       .x(fir_filter_datain),
	       .y(fir_filter_dataout),
	       .output_valid(fir_filter_output_valid)
	       );
   
   umi_fir_filter_output_store
     #(
       .DATA_WIDTH(FIR_FILTER_OUTPUT_DATA_WIDTH)
       )
   filter_output_store (
			.clk(clk),
			.nreset(nreset),
			.fetch_address(udev_req_dstaddr[15:6]),
			.sample_datain(fir_filter_dataout),
			.sample_dataout(output_store_dataout),
			.sample_dataout_valid(output_store_dataout_valid),
			.read_output(output_store_read_enable),
			.write_output(fir_filter_output_valid)
			);
   
   
endmodule // umi_fir_filter
