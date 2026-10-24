# Timing constraints for rtl/sync_fifo.sv (single clock).

# 500 MHz target.
create_clock -name clk -period 2.0 [get_ports clk]

# Clock uncertainty: jitter plus skew budget, applied to setup and hold checks.
set_clock_uncertainty 0.10 [get_clocks clk]

# Inputs arrive 40% into the cycle from upstream logic; outputs must be stable 40% before the
# next edge for downstream logic. Leaves ~60% of the cycle for the FIFO's own paths.
set_input_delay  -clock clk 0.8 [remove_from_collection [all_inputs] [get_ports {clk rst_n}]]
set_output_delay -clock clk 0.8 [all_outputs]

# rst_n is asynchronous assert. Its deassertion is synchronized upstream, so timing it here as a
# data path would only produce false violations.
set_false_path -from [get_ports rst_n]
