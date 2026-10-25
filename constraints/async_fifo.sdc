# Timing constraints for rtl/async_fifo.sv (two unrelated clocks).

create_clock -name wclk -period 2.0 [get_ports wclk]
create_clock -name rclk -period 3.1 [get_ports rclk]

# The clocks have no phase relationship. Every path between them is a Gray-coded pointer into a
# two-flop synchronizer. Do not time those paths as synchronous, but do not cut them either: the
# Gray bits must arrive close together, or the synchronizer can capture a mix of old and new bits.
# Bound each crossing's datapath to the faster clock's period. -datapath_only leaves clock skew out
# of the check, since it means nothing between unrelated clocks.
#
# set_clock_groups -asynchronous and set_false_path are deliberately not used here: both take
# precedence over set_max_delay and would leave the pointer bus unconstrained. Tools with a direct
# bus-skew check (Vivado set_bus_skew) can bound the skew across the pointer bits as well.
set_max_delay -datapath_only 2.0 -from [get_clocks wclk] -to [get_clocks rclk]
set_max_delay -datapath_only 2.0 -from [get_clocks rclk] -to [get_clocks wclk]

set_input_delay  -clock wclk 0.8 [get_ports {push din*}]
set_input_delay  -clock rclk 1.2 [get_ports {pop}]
set_output_delay -clock wclk 0.8 [get_ports full]
set_output_delay -clock rclk 1.2 [get_ports {dout* empty}]

set_false_path -from [get_ports {wrst_n rrst_n}]
