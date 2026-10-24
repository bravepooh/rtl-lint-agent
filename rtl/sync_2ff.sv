// Two-flop synchronizer for a single-bit level signal crossing into clk's domain.
//
// The first flop may go metastable; the second gives it a full cycle to resolve.
// Only for single bits (or Gray-coded buses where one bit changes per step).
// Never synchronize a binary multi-bit bus bit by bit: the bits can land on different cycles.

module sync_2ff (
  input  logic clk,
  input  logic rst_n,
  input  logic d,
  output logic q
);

  logic meta;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      meta <= 1'b0;
      q    <= 1'b0;
    end else begin
      meta <= d;
      q    <= meta;
    end
  end

endmodule
