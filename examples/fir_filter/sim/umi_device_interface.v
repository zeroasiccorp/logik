//umi_device_interface.v
//Peter Grossmann
//31 October 2023
//$Id$
//$Log$

module umi_device_interface
  # (
     parameter DW=256,
     parameter AW=64,
     parameter CW=32,
     parameter UMI_RX_QUEUE = "client2rtl.q",
     parameter UMI_TX_QUEUE = "rtl2client.q"
     )
   (
    input 	    clk,
    
    input 	    umi_req_ready,
    output [CW-1:0] umi_req_cmd,
    output [DW-1:0] umi_req_data,
    output [AW-1:0] umi_req_dstaddr,
    output [AW-1:0] umi_req_srcaddr,
    output 	    umi_req_valid,

    output 	    umi_resp_ready,
    input [CW-1:0]  umi_resp_cmd,
    input [DW-1:0]  umi_resp_data,
    input [AW-1:0]  umi_resp_dstaddr,
    input [AW-1:0]  umi_resp_srcaddr,
    input 	    umi_resp_valid
    );
   
   umi_rx_sim #(
                .VALID_MODE_DEFAULT(2),
                .DW(DW)
                )
   umi_rx_i (
            .clk(clk),
            .data(umi_req_data[DW-1:0]),
            .srcaddr(umi_req_srcaddr),
            .dstaddr(umi_req_dstaddr),
            .cmd(umi_req_cmd),
            .ready(umi_req_ready),
            .valid(umi_req_valid)
            );

   umi_tx_sim #(
                .READY_MODE_DEFAULT(2),
                .DW(DW)
                )
   umi_tx_i (
            .clk(clk),
            .data(umi_resp_data),
            .srcaddr(umi_resp_srcaddr),
            .dstaddr(umi_resp_dstaddr),
            .cmd(umi_resp_cmd),
            .ready(umi_resp_ready),
            .valid(umi_resp_valid)
            );

   integer 	     ready_mode;
   integer 	     valid_mode;
   
   initial begin
      
      /* verilator lint_off IGNOREDRETURN */

      if (!$value$plusargs("valid_mode=%d", valid_mode)) begin
         valid_mode = 2;  // default if not provided as a plusarg
      end

      if (!$value$plusargs("ready_mode=%d", ready_mode)) begin
         ready_mode = 2;  // default if not provided as a plusarg
      end

      $display("umi_device_interface: Initialize Switchboard Queue %s", UMI_RX_QUEUE);
      umi_rx_i.init(UMI_RX_QUEUE);
      umi_rx_i.set_valid_mode(valid_mode);

      $display("umi_device_interface: Initialize Switchboard Queue %s", UMI_TX_QUEUE);
      umi_tx_i.init(UMI_TX_QUEUE);
      umi_tx_i.set_ready_mode(ready_mode);

      /* verilator lint_on IGNOREDRETURN */
   end

endmodule // umi_device_interface
