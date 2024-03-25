//fir_filter_stimulus.v
//Peter Grossmann
//6 October 2023
//$Id$
//$Log$

module fir_filter_stimulus
  # ( 
      parameter TEST_DATA_WIDTH=16,
      parameter TEST_NUM_COEFFS=16,
      parameter TEST_OUTPUT_WIDTH=2*TEST_DATA_WIDTH+$clog2(TEST_NUM_COEFFS),
      parameter NUM_VECTORS = 65536,
      parameter VECTOR_ADDR_BITS = $clog2(NUM_VECTORS)
      )
   ( 
     input 				  clk,
     input 				  resetn,
     input [(VECTOR_ADDR_BITS-1):0] 	  vector_address,
     output [(TEST_DATA_WIDTH-1):0] 	  a,
     output reg [(TEST_OUTPUT_WIDTH-1):0] y
     );

   reg [(TEST_DATA_WIDTH-1):0] 	    vector_memory[0:(NUM_VECTORS-1)];
   reg [(TEST_OUTPUT_WIDTH-1):0]    output_memory[0:(NUM_VECTORS-1)];
   
   reg [(TEST_DATA_WIDTH-1):0] 	    a_vector;
   reg [(TEST_OUTPUT_WIDTH-1):0]    output_vector;

   initial $readmemb("fir_filter_input_vectors.dat", vector_memory);
   initial $readmemb("fir_filter_output_vectors.dat", output_memory);

   assign a = a_vector;

   reg [(TEST_OUTPUT_WIDTH-1):0]    output_vector_sync;
   
   always @(posedge clk or negedge resetn) begin
      if (~resetn) begin
	 output_vector_sync <= 'h0;
	 y <= 'h0;
      end
      else begin
	 output_vector_sync <= output_vector;
	 y <= output_vector_sync;
      end
   end
   
   always @(posedge clk or negedge resetn) begin
      if (~resetn) a_vector <= 'h0;
      else a_vector <= vector_memory[vector_address];
   end

   always @(posedge clk or negedge resetn) begin
      if (~resetn) output_vector <= 'h0;
      else output_vector <= output_memory[vector_address];
   end

endmodule // fir_filter_stimulus

