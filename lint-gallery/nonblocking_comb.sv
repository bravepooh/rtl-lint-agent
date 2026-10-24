// RULE: blocking (=) in combinational logic.
// '<=' in always_comb delays the update to the end of the time step; later reads in the same
// block see stale values.
module nonblocking_comb (
  input  logic [3:0] a, b,
  output logic [3:0] y
);
  logic [3:0] t;
  always_comb begin
    t <= a & b;
    y <= t | a;
  end
endmodule
