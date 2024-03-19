module umi_adder
  #(
    parameter CW = 32,
    parameter AW = 64, 
    parameter DW = 32
    )
   (
    input 		    nreset,
    input 		    clk,
    // Host port (per clink)
    /*
    output 		    user_uhost_req_valid,
    output [CW-1:0]  user_uhost_req_cmd,
    output [AW-1:0] user_uhost_req_dstaddr,
    output [AW-1:0] user_uhost_req_srcaddr,
    output [DW-1:0] user_uhost_req_data,
    input 		    user_uhost_req_ready,

    input 		    uhost_resp_valid,
    input [CW-1:0]   uhost_resp_cmd,
    input [AW-1:0]  uhost_resp_dstaddr,
    input [AW-1:0]  uhost_resp_srcaddr,
    input [DW-1:0]  uhost_resp_data,
    output 		    uhost_resp_ready,
     */
    // Device port
    input 		    user_udev_req_valid,
    input [CW-1:0]   user_udev_req_cmd,
    input [AW-1:0]  user_udev_req_dstaddr,
    input [AW-1:0]  user_udev_req_srcaddr,
    input [DW-1:0]  user_udev_req_data,
    output 		    user_udev_req_ready,
    
    output 		    user_udev_resp_valid,
    output [CW-1:0]  user_udev_resp_cmd,
    output [AW-1:0] user_udev_resp_dstaddr,
    output [AW-1:0] user_udev_resp_srcaddr,
    output [DW-1:0] user_udev_resp_data,
    input 		    user_udev_resp_ready,    

    // output wire [15:0] debug    
    );
    
    // declare memory interface wires and umi endpoint
    // UMI endpoint

    wire [AW-1:0] loc_addr;
    wire          loc_write;
    wire          loc_read;
    wire [7:0]    loc_opcode;
    wire [2:0]    loc_size;
    wire [7:0]    loc_len;
    wire [DW-1:0] loc_wrdata;
    reg  [DW-1:0] loc_rddata;
    wire          loc_ready;

    assign loc_ready = nreset;

    // assign debug signals
    // assign debug = 16'hFFFF;


    // reg [DW-1:0] data;

    umi_endpoint #(
        .CW(CW),
        .AW(AW),
        .DW(DW)
    ) umi_endpoint_i (
        .clk(clk),
        .nreset(nreset),
        .udev_req_valid(user_udev_req_valid),
        .udev_req_cmd(user_udev_req_cmd[CW-1:0]),
        .udev_req_dstaddr(user_udev_req_dstaddr[AW-1:0]),
        .udev_req_srcaddr(user_udev_req_srcaddr[AW-1:0]),
        .udev_req_data(user_udev_req_data[DW-1:0]),
        .udev_req_ready(user_udev_req_ready),
        .udev_resp_valid(user_udev_resp_valid),
        .udev_resp_cmd(user_udev_resp_cmd[CW-1:0]),
        .udev_resp_dstaddr(user_udev_resp_dstaddr[AW-1:0]),
        .udev_resp_srcaddr(user_udev_resp_srcaddr[AW-1:0]),
        .udev_resp_data(user_udev_resp_data[DW-1:0]),
        .udev_resp_ready(user_udev_resp_ready),
        .loc_addr(loc_addr),
        .loc_write(loc_write),
        .loc_read(loc_read),
        .loc_opcode(loc_opcode),
        .loc_size(loc_size),
        .loc_len(loc_len),
        .loc_wrdata(loc_wrdata),
        .loc_rddata(loc_rddata),
        .loc_ready(loc_ready)
    );

    // custom logic

    reg [DW-1:0] a;
    reg [DW-1:0] b;
    
    wire [DW-1:0] c;
    assign c = a + b;

    always @(posedge clk) begin
        if (!nreset) begin
            loc_rddata <= 'b0;
        end else begin
            if (loc_read) begin
                if (loc_addr[7:0] == 8'h00) begin
                    loc_rddata <= a;
                end else if (loc_addr[7:0] == 8'h08) begin
                    loc_rddata <= b;
                end else if (loc_addr[7:0] == 8'h10) begin
                    loc_rddata <= c;
                end
            end else begin
                loc_rddata <= 'b0;
            end
        end
    end

    always @(posedge clk) begin
        if (!nreset) begin
            a <= 'b0;
            b <= 'b0;
        end else if (loc_write) begin
            if (loc_addr[7:0] == 8'h00) begin
                a <= loc_wrdata[DW-1:0];
            end else if (loc_addr[7:0] == 8'h008) begin
                b <= loc_wrdata[DW-1:0];
            end
        end
    end

endmodule // umi_loopback
