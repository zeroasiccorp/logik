/*******************************************************************************
 * Copyright 2024 Zero ASIC Corporation
 *
 * Licensed under the MIT License (see LICENSE for details)
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
