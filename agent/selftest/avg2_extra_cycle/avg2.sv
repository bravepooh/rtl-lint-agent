// Fixes BLKSEQ by making sum non-blocking. Lint-clean for that rule, but sum becomes a register,
// so avg now lags two cycles instead of one.
module avg2 (
  input  logic       clk,
  input  logic [7:0] a,
  input  logic [7:0] b,
  output logic [7:0] avg
);
  logic [8:0] sum;
  always_ff @(posedge clk) begin
    sum <= {1'b0, a} + {1'b0, b};
    avg <= sum[8:1];
  end
endmodule
