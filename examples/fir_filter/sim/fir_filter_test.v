//fir_filter_test.v
//Peter Grossmann
//6 October 2023
//$Id$
//$Log$

module fir_filter_test
  # ( 
      parameter TEST_DATA_WIDTH = 16,
      parameter TEST_NUM_COEFFS = 8,
      parameter TEST_OUTPUT_WIDTH=2*TEST_DATA_WIDTH+$clog2(TEST_NUM_COEFFS),
      parameter VECTOR_COUNTER_BITS=$clog2(`VECTOR_COUNT_MAX)+1
      )
   ( 
     input  clk,
     input  resetn,
     input  input_valid,
     output error
     );

   reg [(VECTOR_COUNTER_BITS-1):0] vector_counter;

   wire [(TEST_DATA_WIDTH-1):0]    a;
   wire [(TEST_OUTPUT_WIDTH-1):0]  y_expected;
   wire [(TEST_OUTPUT_WIDTH-1):0]  y_received;
   wire 			   output_valid;

   integer 			   errors;

   initial errors = 0;
   always @(negedge clk) begin
      if (error) errors <= errors + 1;
   end
   
`ifdef VCD_DUMP
   initial begin
      $dumpfile("fir_filter.vcd");
      $dumpvars(0, fir_filter_test);
   end
`endif

   always @(posedge clk or negedge resetn) begin
     if (~resetn) begin
	vector_counter <= 'h0;
     end
     else if (input_valid) begin
	vector_counter <= vector_counter + 1;
     end
   end
   
   always@(*) begin
      if (vector_counter == `VECTOR_COUNT_MAX+3) begin
`ifdef VCD_DUMP
	 $dumpoff;
`endif
	 if (errors == 0) begin
	    $display("PASS");
	 end
	 else begin
	    $display("FAIL");
	 end
	 $finish;
      end
   end

   reg input_valid_sync;
   
   always @(posedge clk or negedge resetn) begin
      if (~resetn) begin
	 input_valid_sync <= 1'b0;
      end
      else begin
	 input_valid_sync <= input_valid;
      end
   end
   
   assign error = output_valid && (y_expected != y_received);
   
   fir_filter_wrapper
     #(
       .DATA_WIDTH(TEST_DATA_WIDTH),
       .NUM_TAPS(TEST_NUM_COEFFS)
       ) 
   dut (
	.clk(clk),
	.resetn(resetn),
	.input_valid(input_valid_sync),
	.x(a),
	.y(y_received),
	.output_valid(output_valid)
	);

   fir_filter_stimulus 
     #(
       .TEST_DATA_WIDTH(TEST_DATA_WIDTH),
       .TEST_NUM_COEFFS(TEST_NUM_COEFFS),
       .NUM_VECTORS(`VECTOR_COUNT_MAX)
       ) 
   stimulus (
	     .clk(clk),
	     .resetn(resetn),
	     .vector_address(vector_counter[(VECTOR_COUNTER_BITS-2):0]),
	     .a(a), 
	     .y(y_expected)
	     );

endmodule // fir_filter_test
