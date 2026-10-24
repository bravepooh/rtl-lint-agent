// Divide a 12-bit value by 16, rounding half up: q = floor((x + 8) / 16). Range 0..256, so q is
// 9 bits. Every input value is legal, including the top of the range.
module round_div16 (
  input  logic [11:0] x,
  output logic [8:0]  q
);
  assign q = (x + 8) >> 4;
endmodule
