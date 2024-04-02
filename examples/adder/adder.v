module adder #(DW = 8)
   (
    input [DW-1:0]  a,
    input [DW-1:0]  b,
    output [DW-1:0] y
    );

   assign y = a + b;

endmodule
