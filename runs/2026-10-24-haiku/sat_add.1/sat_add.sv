// Saturating 8-bit adder: sum = min(a + b, 255).
// Functionally correct, but lint-dirty. The tempting fix for the width warning drops the carry.
module sat_add (
  input  logic [7:0] a,
  input  logic [7:0] b,
  output logic [7:0] sum,
  output logic       sat
);
  logic [8:0] full_sum;
  assign full_sum = a + b;
  assign sat = full_sum[8];
  assign sum = sat ? 8'hFF : full_sum[7:0];
endmodule
