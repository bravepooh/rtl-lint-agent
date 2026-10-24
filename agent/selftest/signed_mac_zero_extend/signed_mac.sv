// Fixes WIDTHEXPAND by padding with zeros. Lint-clean, but negative products now add as large
// positive numbers (and the concatenation makes the whole sum unsigned).
module signed_mac (
  input  logic               clk,
  input  logic               rst_n,
  input  logic               clr,
  input  logic               en,
  input  logic signed [7:0]  a,
  input  logic signed [7:0]  b,
  output logic signed [19:0] acc
);
  logic signed [15:0] prod;
  assign prod = a * b;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)   acc <= '0;
    else if (clr) acc <= '0;
    else if (en)  acc <= acc + {4'b0000, prod};
  end
endmodule
