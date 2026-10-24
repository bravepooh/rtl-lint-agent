// RULE: no inferred latches.
// always_comb with an if and no else leaves q unassigned on one path, so the tool keeps the old
// value with a level-sensitive latch. Latches break static timing assumptions and scan.
module latch (
  input  logic       en,
  input  logic [3:0] d,
  output logic [3:0] q
);
  always_comb begin
    if (en) q = d;
  end
endmodule
