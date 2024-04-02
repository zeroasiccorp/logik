/*******************************************************************************
 * Copyright 2024 Zero ASIC Corporation
 *
 * Licensed under the MIT License (see LICENSE for details)
 ******************************************************************************/

module adder
  # (
     parameter DATA_WIDTH = 8
     )
   (
    input [(DATA_WIDTH-1):0] a,
    input [(DATA_WIDTH-1):0] b,
    output [(DATA_WIDTH):0] y
    );

   assign y = a + b;

endmodule // adder
