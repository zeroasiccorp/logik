create_clock -period 50.0 clk
set_input_delay -clock clk [ get_ports * ] 5.0
set_output_delay -clock clk [ get_ports * ] 5.0
set_clock_uncertainty 1.0
set_clock_latency -source 1.0 [ get_clocks clk ]

