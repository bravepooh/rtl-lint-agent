// RULE: one module per file, named like the file.
// Tools and humans find modules by filename. This file holds module "adder".
module adder (
  input  logic [3:0] a, b,
  output logic [4:0] s
);
  assign s = a + b;
endmodule
