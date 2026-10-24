// Two-stage delay line: q = d delayed by two clocks.
// Written with blocking assignments in reverse order, which happens to simulate correctly.
module pipe_delay (
  input  logic       clk,
  input  logic [3:0] d,
  output logic [3:0] q
);
  logic [3:0] s1;
  always_ff @(posedge clk) begin
    q  <= s1;
    s1 <= d;
  end
endmodule
