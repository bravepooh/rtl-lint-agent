// Registered average of two unsigned samples: avg = (a + b) / 2, rounded down.
// Latency is exactly one clock: avg reflects the a and b sampled at the previous edge.
module avg2 (
  input  logic       clk,
  input  logic [7:0] a,
  input  logic [7:0] b,
  output logic [7:0] avg
);
  logic [8:0] sum;
  always_comb begin
    sum = {1'b0, a} + {1'b0, b};
  end
  always_ff @(posedge clk) begin
    avg <= sum[8:1];
  end
endmodule
