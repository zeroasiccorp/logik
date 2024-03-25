// testbench.sv - umi_fir_filter_test
//Peter Grossmann
//6 October 2023
//$Id$
//$Log$

module testbench
  # (
     parameter DW=128,
     parameter AW=64,
     parameter CW=32
     )
   (
     input  clk
     );

   wire         resetn;
   reg [7:0]    resetn_vec = 8'b00;

   assign resetn = resetn_vec[7];

   always @(posedge clk)
       resetn_vec <= {resetn_vec[6:0], 1'b1};

   reg [31:0] timeout_counter;

   always @(posedge clk or negedge resetn) begin
      if (~resetn) begin
	 timeout_counter <= 'h0;
      end
      else begin
	 timeout_counter <= timeout_counter + 1;
      end
   end

   always@(*) begin
      if (timeout_counter == 100*`VECTOR_COUNT_MAX) begin
	 $display("TIMEOUT");
	 $finish;
      end
   end

   wire 	     udev_req_valid;
   wire [CW-1:0]     udev_req_cmd;
   wire [AW-1:0]     udev_req_dstaddr;
   wire [AW-1:0]     udev_req_srcaddr;
   wire [DW-1:0]     udev_req_data;
   wire 	     udev_req_ready;

   wire 	     udev_resp_valid;
   wire [CW-1:0]     udev_resp_cmd;
   wire [AW-1:0]     udev_resp_dstaddr;
   wire [AW-1:0]     udev_resp_srcaddr;
   wire [DW-1:0]     udev_resp_data;
   wire 	     udev_resp_ready;

   umi_device_interface
     #(
       .DW(128)
       )
   umi_device_interface (
			 .clk(clk),
			 .umi_req_valid(udev_req_valid),
			 .umi_req_cmd(udev_req_cmd),
			 .umi_req_dstaddr(udev_req_dstaddr),
			 .umi_req_srcaddr(udev_req_srcaddr),
			 .umi_req_data(udev_req_data),
			 .umi_req_ready(udev_req_ready),
			 .umi_resp_valid(udev_resp_valid),
			 .umi_resp_cmd(udev_resp_cmd),
			 .umi_resp_dstaddr(udev_resp_dstaddr),
			 .umi_resp_srcaddr(udev_resp_srcaddr),
			 .umi_resp_data(udev_resp_data),
			 .umi_resp_ready(udev_resp_ready)
			 );

   umi_fir_filter
   dut (
	.clk(clk),
	.nreset(resetn),
	.udev_req_valid(udev_req_valid),
	.udev_req_cmd(udev_req_cmd),
	.udev_req_dstaddr(udev_req_dstaddr),
	.udev_req_srcaddr(udev_req_srcaddr),
	.udev_req_data(udev_req_data),
	.udev_req_ready(udev_req_ready),
	.udev_resp_valid(udev_resp_valid),
	.udev_resp_cmd(udev_resp_cmd),
	.udev_resp_dstaddr(udev_resp_dstaddr),
	.udev_resp_srcaddr(udev_resp_srcaddr),
	.udev_resp_data(udev_resp_data),
	.udev_resp_ready(udev_resp_ready)
	);

endmodule // umi_fir_filter_test
