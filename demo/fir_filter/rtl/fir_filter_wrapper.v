//fir_filter_wrapper.v
//Peter Grossmann
//7 October 2023
//$Id$
//$Log$

`define FIR_FILTER_CONSTANT_COEFFS

module fir_filter_wrapper
  #(
    parameter DATA_WIDTH = 16,
    parameter NUM_TAPS = 8,
    parameter OUTPUT_WIDTH = 2*DATA_WIDTH+$clog2(NUM_TAPS)
    )
   (
    input 			    clk,
    input 			    resetn,
    input 			    input_valid,
    input [(DATA_WIDTH-1):0] 	    x,
    output reg [(OUTPUT_WIDTH-1):0] y,
    output reg 			    output_valid
    );


   wire [(NUM_TAPS*DATA_WIDTH-1):0] coeff;

   assign coeff = {
		   16'h0001,
		   16'h0002,
		   16'h0004,
		   16'h0008,
		   16'h0008,
		   16'h0004,
		   16'h0002,
		   16'h0001
		   };
   
   fir_filter 
     #(
       .DATA_WIDTH(DATA_WIDTH),
       .COEFF_WIDTH(DATA_WIDTH),
       .NUM_TAPS(NUM_TAPS)
       ) 
   fir_filter (
	       .clk(clk),
	       .resetn(resetn),
	       .input_valid(input_valid),
	       .coeff(coeff),
	       .x(x),
	       .y(y),
	       .output_valid(output_valid)
	       );


endmodule // fir_filter_wrapper
