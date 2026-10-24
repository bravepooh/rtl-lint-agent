// RULE: no silent truncation.
// a + b is 9 bits wide (the carry), sum is 8. The carry is dropped without anyone deciding to.
module width_trunc (
  input  logic [7:0] a,
  input  logic [7:0] b,
  output logic [7:0] sum
);
  assign sum = {1'b0, a} + {1'b0, b};
endmodule
