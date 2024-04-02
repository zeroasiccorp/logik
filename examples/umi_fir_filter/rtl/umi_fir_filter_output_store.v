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

module umi_fir_filter_output_store
  # (
     parameter DATA_WIDTH = 32,
     parameter NUM_SAMPLES = 1024,
     parameter ADDR_WIDTH = $clog2(NUM_SAMPLES)
     )
   (
    input 			  clk,
    input 			  nreset,
    input [(ADDR_WIDTH-1):0] 	  fetch_address,
    input [(DATA_WIDTH-1):0] 	  sample_datain,
    output reg [(DATA_WIDTH-1):0] sample_dataout,
    output reg 			  sample_dataout_valid,
    input 			  read_output,
    input 			  write_output
    );


   reg [(DATA_WIDTH-1):0]     output_store[0:(NUM_SAMPLES-1)];
   reg [(ADDR_WIDTH-1):0]     store_address;

   always @(posedge clk or negedge nreset) begin
      if (~nreset) begin
	 store_address <= 'h0;
      end
      else begin
	 if (write_output) begin
	    store_address <= store_address + 1;
	 end
      end
   end

   always @(posedge clk) begin
      if (write_output) begin
	 output_store[store_address] <= sample_datain;
      end
      if (read_output) begin
	 sample_dataout <= output_store[fetch_address];
      end
   end	 

   always @(posedge clk) begin
      if (read_output) begin
	 sample_dataout_valid <= 1'b1;
      end
      else begin
	 sample_dataout_valid <= 1'b0;
      end
   end
   
endmodule // umi_fir_filter_output_store
