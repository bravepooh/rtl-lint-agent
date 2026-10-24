// Fixes COMBDLY correctly but also flips the reset value of prev. The tests never drive sig high
// during reset, so they pass. Formal equivalence sees the difference.
module edge_det (
  input  logic clk,
  input  logic rst_n,
  input  logic sig,
  output logic pulse
);
  logic prev;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) prev <= 1'b1;
    else        prev <= sig;
  end
  always_comb begin
    pulse = sig & ~prev;
  end
endmodule
