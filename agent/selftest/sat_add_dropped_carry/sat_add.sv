// Plausible fix for the width warnings that silently drops the carry: a + b is evaluated
// at 8 bits inside the concatenation, then zero-extended. Lint-clean, functionally wrong.
module sat_add (
  input  logic [7:0] a,
  input  logic [7:0] b,
  output logic [7:0] sum,
  output logic       sat
);
  logic [8:0] full_sum;
  assign full_sum = {1'b0, a + b};
  assign sat = full_sum[8];
  assign sum = sat ? 8'hFF : full_sum[7:0];
endmodule
