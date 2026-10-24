# Timing constraints for rtl/async_fifo.sv (two unrelated clocks).

create_clock -name wclk -period 2.0 [get_ports wclk]
create_clock -name rclk -period 3.1 [get_ports rclk]

# The clocks have no phase relationship. Every path between them goes through a two-flop
# synchronizer on a Gray-coded pointer, so the timer must not try to time them.
set_clock_groups -asynchronous -group [get_clocks wclk] -group [get_clocks rclk]

# But the Gray pointer bits must still arrive close together, or the synchronizer can capture a
# mix of old and new bits. Bound the skew across the bus to less than one destination period.
set_max_delay -datapath_only 2.0 -from [get_clocks wclk] -to [get_clocks rclk]
set_max_delay -datapath_only 2.0 -from [get_clocks rclk] -to [get_clocks wclk]

set_input_delay  -clock wclk 0.8 [get_ports {push din*}]
set_input_delay  -clock rclk 1.2 [get_ports {pop}]
set_output_delay -clock wclk 0.8 [get_ports full]
set_output_delay -clock rclk 1.2 [get_ports {dout* empty}]

set_false_path -from [get_ports {wrst_n rrst_n}]
