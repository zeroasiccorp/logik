//dp_memory_generic.v
//Peter Grossmann
//18 October 2023
//$Id$
//$Log$

module dp_memory_generic 
  # (
     parameter ADDRESS_WIDTH = 12,
     parameter DATA_WIDTH = 32
     )
   (
    input 			  clk,
    input 			  ce_a,
    input 			  ce_b,
    input 			  we,
    input 			  re,
    input [(ADDRESS_WIDTH-1):0]   addr_a,
    input [(ADDRESS_WIDTH-1):0]   addr_b,
    input [(DATA_WIDTH-1):0] 	  datain,
    output reg [(DATA_WIDTH-1):0] dataout
    );

   // Test Yosys's recommended coding style for
   // true dual port memories with different clocks
   // and exclusive read/write
   
   reg [DATA_WIDTH-1:0] 	  ram[(2**ADDRESS_WIDTH)-1:0];

   //This is ripped straight from
   //https://yosyshq.readthedocs.io/projects/yosys/en/latest/CHAPTER_Memorymap.html#true-dual-port-tdp-patterns
   //modified only to match our desired port naming convention

   //***NOTE:  This logic is NOT identical to the lambdalib instance above;
   //          when we actually support the above ifdef that should be rectified
   
   always @(posedge clk) begin
      if (we && ce_a)
        ram[addr_a] <= datain;
   end

   always @(posedge clk) begin
      if (re && ce_b)
        dataout <= ram[addr_b];
   end

endmodule // memory_generic
