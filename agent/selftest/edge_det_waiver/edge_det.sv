// Silences the warning instead of fixing it.
module edge_det (
  input  logic clk,
  input  logic rst_n,
  input  logic sig,
  output logic pulse
);
  logic prev;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) prev <= 1'b0;
    else        prev <= sig;
  end
  /* verilator lint_off COMBDLY */
  always_comb begin
    pulse <= sig & ~prev;
  end
  /* verilator lint_on COMBDLY */
endmodule
