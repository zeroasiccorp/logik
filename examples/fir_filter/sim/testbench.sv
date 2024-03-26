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

   localparam FF_RX_QUEUE = "client2rtl.q";
   localparam FF_TX_QUEUE = "rtl2client.q";

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
      if (timeout_counter == 200*`VECTOR_COUNT_MAX) begin
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

    /////////////////////////////////////////////////////
    // switchboard connections to FIR FILTER UMI ports //
    /////////////////////////////////////////////////////

    // Python is the UMI host
    // FIR Filter is the UMI device

    queue_to_umi_sim #(
        .VALID_MODE_DEFAULT(2),
        .DW(DW)
    ) host2ff_i (
        .clk            (clk),
        .valid          (udev_req_valid),
        .cmd            (udev_req_cmd),
        .dstaddr        (udev_req_dstaddr),
        .srcaddr        (udev_req_srcaddr),
        .data           (udev_req_data[DW-1:0]),
        .ready          (udev_req_ready)
    );

    umi_to_queue_sim #(
        .READY_MODE_DEFAULT(2),
        .DW(DW)
    ) ff2host_i (
        .clk            (clk),
        .valid          (udev_resp_valid),
        .cmd            (udev_resp_cmd),
        .dstaddr        (udev_resp_dstaddr),
        .srcaddr        (udev_resp_srcaddr),
        .data           (udev_resp_data[DW-1:0]),
        .ready          (udev_resp_ready)
    );

    // initialize switchboard connections

    initial begin
        /* verilator lint_off IGNOREDRETURN */

        // get runtime options indicating the desired behavior of
        // ready/valid handshaking by switchboard modules. for more
        // details, see https://github.com/zeroasiccorp/switchboard/tree/main/examples/umiram

        integer valid_mode, ready_mode;

        if (!$value$plusargs("valid_mode=%d", valid_mode)) begin
           valid_mode = 2;  // default if not provided as a plusarg
        end

        if (!$value$plusargs("ready_mode=%d", ready_mode)) begin
           ready_mode = 2;  // default if not provided as a plusarg
        end

        /////////////////////////////////
        // switchboard queues for GPIO //
        /////////////////////////////////

        // queue names must match definitions in
        // the Python test script (umi_fir_filter_test.py)

        $display("umi_device_interface: Initialize Switchboard Queue %s", FF_RX_QUEUE);
        host2ff_i.init(FF_RX_QUEUE);
        host2ff_i.set_valid_mode(valid_mode);

        $display("umi_device_interface: Initialize Switchboard Queue %s", FF_TX_QUEUE);
        ff2host_i.init(FF_TX_QUEUE);
        ff2host_i.set_ready_mode(ready_mode);

        /* verilator lint_on IGNOREDRETURN */
    end

endmodule // umi_fir_filter_test
