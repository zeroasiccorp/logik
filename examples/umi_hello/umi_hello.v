/*******************************************************************************
 * Copyright 2024 Zero ASIC Corporation
 *
 * Licensed under the MIT License (see LICENSE for details)
 ******************************************************************************/

module umi_hello #(
    parameter CMD_WIDTH = 32,
    parameter ADDR_WIDTH = 64, 
    parameter DATA_WIDTH = 128
) (
    input nreset,
    input clk,

    // UMI host
    output reg uhost_req_valid = 0,
    output reg [CMD_WIDTH-1:0]  uhost_req_cmd = 0,
    output reg [ADDR_WIDTH-1:0] uhost_req_dstaddr = 0,
    output [ADDR_WIDTH-1:0] uhost_req_srcaddr,
    output reg [DATA_WIDTH-1:0] uhost_req_data = 0,
    input uhost_req_ready,

    // UMI device (unused)
    input udev_req_valid,
    input [CMD_WIDTH-1:0] udev_req_cmd,
    input [ADDR_WIDTH-1:0] udev_req_dstaddr,
    input [ADDR_WIDTH-1:0] udev_req_srcaddr,
    input [DATA_WIDTH-1:0] udev_req_data,
    output udev_req_ready
);
    // message to print

    localparam MESSAGE = "Hello World!\n";
    localparam LENGTH = $bits(MESSAGE) / 8;

    // address where characters should be sent (implemented in
    // the emulation infrastructure)

    localparam [63:0] PUTC_ADDR = 'h1000000;

    // walk through the message, printing out each character

    reg [31:0] count = 0;

    always @(posedge clk) begin
        if (!nreset) begin
            count <= 0;
            uhost_req_valid <= 0;
        end else if (uhost_req_valid && uhost_req_ready) begin
            count <= count + 1;
            uhost_req_valid <= 1'b0;
        end else begin
            if (count <= (LENGTH - 1)) begin
                uhost_req_valid <= 'b1;
                uhost_req_cmd <= 'h5;  // posted write
                uhost_req_dstaddr <= PUTC_ADDR;
                uhost_req_data[7:0] <= MESSAGE[8 * (LENGTH - 1 - count) +: 8];
            end else begin
                uhost_req_valid <= 'b0;
            end
        end
    end

    // srcaddr is unused since these are posted writes

    assign uhost_req_srcaddr = 0;

    // device port is unused

    assign udev_req_ready = 1'b0;

endmodule
