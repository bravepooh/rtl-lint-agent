// RULE: every case has a default (or is provably complete).
// sel = 2'b11 is not covered, so y holds its value: an inferred latch through the back door.
module case_incomplete (
  input  logic [1:0] sel,
  input  logic [3:0] a, b, c,
  output logic [3:0] y
);
  always_comb begin
    case (sel)
      2'b00: y = a;
      2'b01: y = b;
      2'b10: y = c;
    endcase
  end
endmodule
