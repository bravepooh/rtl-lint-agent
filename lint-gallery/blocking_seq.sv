// RULE: non-blocking (<=) in sequential logic.
// With '=' the second line sees the NEW value of q1, so the two-stage pipeline collapses to
// one stage in simulation. Synthesis may disagree with simulation.
module blocking_seq (
  input  logic clk,
  input  logic d,
  output logic q2
);
  logic q1;
  always_ff @(posedge clk) begin
    q1 = d;
    q2 = q1;
  end
endmodule
