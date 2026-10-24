// Two-stage delay line: q = d delayed by two clocks.
module pipe_delay (
  input  logic       clk,
  input  logic [3:0] d,
  output logic [3:0] q
);
  logic [3:0] s1;
  always_ff @(posedge clk) begin
    s1 <= d;
    q  <= s1;
  end
endmodule
