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
