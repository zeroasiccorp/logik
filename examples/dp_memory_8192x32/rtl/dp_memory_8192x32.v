
module dp_memory_8192x32
(
  input clk,
  input ce_a,
  input we,
  input re,
  input [12:0] addr_a,
  input [31:0] datain,
  output [31:0] dataout,
  input ce_b,
  input [12:0] addr_b
);


  dp_memory_generic
  #(
    .ADDRESS_WIDTH(13),
    .DATA_WIDTH(32)
  )
  dp_memory_8192x32_inst
  (
    .clk(clk),
    .ce_a(ce_a),
    .we(we),
    .re(re),
    .addr_a(addr_a[12:0]),
    .datain(datain[31:0]),
    .dataout(dataout[31:0]),
    .ce_b(ce_b),
    .addr_b(addr_b[12:0])
  );


endmodule
