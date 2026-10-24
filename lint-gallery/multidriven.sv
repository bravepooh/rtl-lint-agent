// RULE: one driver per signal.
// Two processes drive cnt. Simulation picks a winner by scheduling order; synthesis either
// errors or shorts two outputs together.
module multidriven (
  input  logic       clk,
  input  logic       inc,
  input  logic       clr,
  output logic [3:0] cnt
);
  always_ff @(posedge clk) if (inc) cnt <= cnt + 4'd1;
  always_ff @(posedge clk) if (clr) cnt <= 4'd0;
endmodule
