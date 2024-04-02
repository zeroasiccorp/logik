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

module umi_fir_filter_regs
  #(
    parameter ADDR_WIDTH = 2,
    parameter DATA_WIDTH = 128
    )
   (
    input 			  clk,
    input 			  nreset,
    input 			  write,
    input 			  read,
    
    input [(ADDR_WIDTH-1):0] 	  address,
    input [(DATA_WIDTH-1):0] 	  datain,
    output reg [(DATA_WIDTH-1):0] dataout,
    output [(DATA_WIDTH-1):0] 	  coeff
    );

`include "umi_fir_filter_regs.vh"
   
   reg [(DATA_WIDTH-1):0]     ctrl_reg;
   reg [(DATA_WIDTH-1):0]     coeff_reg;

   wire 		      ctrl_reg_write;
   wire 		      coeff_reg_write;

   assign coeff = coeff_reg;
   
   assign ctrl_reg_write = write && (address == CTRL_REG_ADDR);
   assign coeff_reg_write = write && (address == COEFF_REG_ADDR);
   
   always @(posedge clk or negedge nreset) begin
      if (~nreset) begin
	 ctrl_reg <= 'h0;
	 coeff_reg <= 'h0;
      end
      else begin
	 if (ctrl_reg_write) begin
	    ctrl_reg <= datain;
	 end
	 if (coeff_reg_write) begin
	    coeff_reg <= datain;
	 end
      end // else: !if(~nreset)
   end // always @ (posedge clk or negedge nreset)

   always @(*) begin
      case(address)
	CTRL_REG_ADDR: dataout = ctrl_reg;
	COEFF_REG_ADDR: dataout = coeff_reg;
	default: dataout = 'h0;
      endcase // case (address)
   end
      
endmodule
