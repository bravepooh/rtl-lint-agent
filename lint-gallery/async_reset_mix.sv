// RULE: a reset is either synchronous or asynchronous, not both.
// rst_n is an async reset for q but used as plain data for r. Reset trees and STA treat
// async resets specially; mixing confuses both.
module async_reset_mix (
  input  logic clk,
  input  logic rst_n,
  input  logic d,
  output logic q,
  output logic r
);
  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) q <= 1'b0; else q <= d;
  always_ff @(posedge clk)
    if (!rst_n) r <= 1'b0; else r <= d;
endmodule
