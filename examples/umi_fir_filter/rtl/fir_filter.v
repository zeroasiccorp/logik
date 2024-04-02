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

//This module implements a simple N-tap FIR filter
//The goal is to provide a very explicit, clear, flexible
//implementation of the canonical FIR filter equation.

//Wikipedia was used for reference for the mathematics:
//https://en.wikipedia.org/wiki/Finite_impulse_response

//Because this circuit is used primarily for FPGA benchmarking,
//it contains an ifdef wrapper for a define SYNC_RESET that
//is used for academic exercises where the FPGA architecture may
//be so simple that it does not support asynchronous resets
//Since modern FPGAs to support this construct, asynchronous resets
//are used by default

module fir_filter
  # (
     parameter COEFF_WIDTH = 16,
     parameter DATA_WIDTH = 16,
     parameter NUM_TAPS = 16,
     parameter PRODUCT_WIDTH = COEFF_WIDTH + DATA_WIDTH,
     parameter OUTPUT_WIDTH = PRODUCT_WIDTH+$clog2(NUM_TAPS)
     )
   (
    input 				 clk,
    input 				 resetn,
    input 				 input_valid,
`ifdef FIR_FILTER_CONSTANT_COEFFS
    input [(COEFF_WIDTH*NUM_TAPS-1):0] coeff,
`else
    input 				 coeff_valid,
    input [(DATA_WIDTH-1):0] 		 coeff_in,
`endif
    input [(DATA_WIDTH-1):0] 		 x,
    output reg [(OUTPUT_WIDTH-1):0] 	 y,
    output reg 				 output_valid
    );

`ifdef FIR_FILTER_SIMPLE_ADDER
   reg [(OUTPUT_WIDTH-1):0] 		 current_sum;
`else
   reg [(OUTPUT_WIDTH-1):0] 		 current_sum;
`endif
   
   reg [(PRODUCT_WIDTH*NUM_TAPS-1):0] 	 tap_product;

   reg [(DATA_WIDTH*NUM_TAPS-1):0] 	 tap;
`ifdef FIR_FILTER_CONSTANT_COEFFS
`else
   reg [(DATA_WIDTH*NUM_TAPS-1):0] 	 coeff;
`endif
   
   genvar 				 i;

   reg 					 input_valid_sync;
   
   /***************************************************************************
   
    Block to store the input samples.  The approach is to simply take a running
    stream of data from the input port, and rely on valid/user sending zeros
    to delineate between separate sequences
    
    ***************************************************************************/
   
   generate
      for (i = 0; i < NUM_TAPS; i = i + 1) begin : tap_gen
`ifdef SYNC_RESET
	 always @(posedge clk) begin
`else
	 always @(posedge clk or negedge resetn) begin
`endif
	    if (~resetn) begin
	       tap[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)] <= 'h0;
	    end
	    else begin
	      if (input_valid) begin
		 if (i == 0) begin
		    tap[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)] <= x;
		 end
		 else begin
		    tap[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)] 
		      <= tap[(DATA_WIDTH*i-1):(DATA_WIDTH*(i-1))];
		 end
	      end
`ifdef CLEAR_WHEN_INVALID
	      else begin
		 tap[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)] <= 'h0;
	      end // else: !if(input_valid)
`endif
	    end // else: !if(~resetn)
	 end
      end // block: tap_gen
   endgenerate	 

   /***************************************************************************
   
    If we are using coefficients loaded via shift register interface,
    store them using this block.  To ensure that the coefficients are held in
    place after loading, you can only shift them in when you assert the
    coeff_valid signal
    
    ***************************************************************************/
`ifdef FIR_FILTER_CONSTANT_COEFFS
`else

  generate
      for (i = 0; i < NUM_TAPS; i = i + 1) begin : coeff_gen
`ifdef SYNC_RESET
	 always @(posedge clk) begin
`else
	 always @(posedge clk or negedge resetn) begin
`endif
	    if (~resetn) begin
	       coeff[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)] <= 'h0;
	    end
	    else if (coeff_valid) begin
	       if (i == 0) begin
		  coeff[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)] <= coeff_in;
	       end
	       else begin
		  coeff[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)] 
		    <= coeff[(DATA_WIDTH*i-1):(DATA_WIDTH*(i-1))];
	       end
	    end
	 end
      end // block: tap_gen
   endgenerate	 
   
`endif
   
   /***************************************************************************
   
    This block instantiates the multipliers that must be summed for the current
    output sample
    
    ***************************************************************************/
   generate
      for (i = 0; i < NUM_TAPS; i = i + 1) begin : multiplier_gen
	 assign tap_product[(PRODUCT_WIDTH*(i+1)-1):(PRODUCT_WIDTH*i)] 
	   = coeff[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)]
	     * tap[(DATA_WIDTH*(i+1)-1):(DATA_WIDTH*i)];
      end
   endgenerate

   /***************************************************************************
   
    This block computes the running sum.  We do this combinationally, on
    the assumption that the critical path through the running sum adder
    will be roughly the same as the multiplier.
    
    ***************************************************************************/

   //***NOTE:  This coding style relies on synthesis tools to restructure the
   //          adder into a tree for you; make sure that your tools actually do
   //          this!
`ifdef FIR_FILTER_SIMPLE_ADDER
   //***NOTE:  Verilator 4.226 doesn't seem to like this scheme; it wants the
   //          bus indices of the tap_product to be constant
   always@(*) begin
      for (i = 0; i < NUM_TAPS; i = i + 1) begin
	 if (i == 0) begin
	    current_sum = tap_product[(PRODUCT_WIDTH*(i+1)-1):(PRODUCT_WIDTH*i)];
	 end
	 else begin
	    current_sum = current_sum + tap_product[(PRODUCT_WIDTH*(i+1)-1):(PRODUCT_WIDTH*i)];
	 end
      end
   end
`else // !`ifdef FIR_FILTER_SIMPLE_ADDER

   tree_adder
     #(
       .DATA_WIDTH(PRODUCT_WIDTH),
       .NUM_TERMS(NUM_TAPS)
       )
   tree_adder
     (
      .a(tap_product),
      .y(current_sum)
      );
   
`endif
      
   /***************************************************************************
   
    Register the sum for the current output sample here:
    
    ***************************************************************************/
`ifdef SYNC_RESET
   always @(posedge clk) begin
`else
   always @(posedge clk or negedge resetn) begin
`endif
      if (~resetn) begin
	 y <= 'h0;
      end
      else begin
	 y <= current_sum;
      end
   end
   
   /***************************************************************************
   
    Register output valid based on input valid
    
    ***************************************************************************/
`ifdef SYNC_RESET
   always @(posedge clk) begin
`else
   always @(posedge clk or negedge resetn) begin
`endif
      if (~resetn) begin
	 output_valid <= 1'b0;
	 input_valid_sync <= 1'b0;
      end
      else begin
	 input_valid_sync <= input_valid;
	 output_valid <= input_valid_sync;
      end
   end
   
endmodule
