module tree_adder
  # (
     parameter DATA_WIDTH = 16,
     parameter NUM_TERMS = 8,
     parameter NUM_STAGES = +$clog2(NUM_TERMS),
     parameter OUTPUT_WIDTH = DATA_WIDTH+NUM_STAGES
     )
   (
    input [(DATA_WIDTH*NUM_TERMS-1):0] a,
    output [(OUTPUT_WIDTH-1):0] y
    );

   /* verilator lint_off UNOPTFLAT */
   wire [(OUTPUT_WIDTH*(NUM_TERMS-1)-1):0] sum_terms;
   /* verilator lint_on UNOPTFLAT */
   
   genvar 				    stage_i;
   genvar 				    term_i;

   generate
      for (term_i = 0; term_i < NUM_TERMS/2; term_i = term_i + 1) begin
	 
	 /* verilator lint_off WIDTH */
	 assign sum_terms[OUTPUT_WIDTH*(term_i + (1 << (NUM_STAGES-1))-1)+:OUTPUT_WIDTH] 
	   = a[(DATA_WIDTH*(2*term_i+1))+:DATA_WIDTH]
	     + a[(DATA_WIDTH*(2*term_i  ))+:DATA_WIDTH];
	 /* verilator lint_on WIDTH */
	 
      end
   endgenerate
   
   generate
      for (stage_i = 0; stage_i < (NUM_STAGES-1); stage_i = stage_i + 1) begin
	 for (term_i = 0; term_i < (1 << stage_i); term_i = term_i + 1) begin

	    /* verilator lint_off UNOPTFLAT */
	    assign sum_terms[OUTPUT_WIDTH*(term_i + (1 << stage_i) - 1)+:OUTPUT_WIDTH] 
	      = sum_terms[(OUTPUT_WIDTH*(2*term_i + (1 << (stage_i+1)) - 1))+:OUTPUT_WIDTH]
		+ sum_terms[(OUTPUT_WIDTH*(2*term_i + (1 << (stage_i+1))    ))+:OUTPUT_WIDTH];
	    /* verilator lint_on UNOPTFLAT */

	 end
      end
   endgenerate
   
   assign y = sum_terms[(OUTPUT_WIDTH-1):0];

endmodule
