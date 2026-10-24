// Rising-edge detector: pulse is high for one cycle after sig goes 0 -> 1.
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
  always_comb begin
    pulse <= sig & ~prev;
  end
endmodule
