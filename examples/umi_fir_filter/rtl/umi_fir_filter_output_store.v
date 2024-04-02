/*******************************************************************************
 * Copyright 2024 Zero ASIC Corporation
 *
 * Licensed under the MIT License (see LICENSE for details)
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
